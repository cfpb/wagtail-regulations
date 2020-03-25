import logging
import re
from collections import OrderedDict
from datetime import date
from functools import partial
from urllib.parse import urljoin

from django.db import models
from django.http import Http404
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template.response import TemplateResponse

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from regdown import regdown
from wagtailregulations.api.serializers import PartSerializer
from wagtailregulations.models import Part, Section
from wagtailregulations.resolver import get_contents_resolver, get_url_resolver


logger = logging.getLogger(__name__)


class RegulationPageMixin(RoutablePageMixin, models.Model):
    """A routable page mixin for serving a regulation """

    regulation = models.ForeignKey(
        Part,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="page",
    )

    content_panels = [
        FieldPanel("regulation", Part),
    ]

    # Export fields over the API
    api_fields = [
        APIField("regulation", serializer=PartSerializer()),
    ]

    template = "wagtailregulations/regulation_index.html"
    section_template = "wagtailregulations/regulation_section.html"
    versions_template = "wagtailregulations/regulation_versions.html"
    interpretation_template = "wagtailregulations/inline_interpretations.html"

    class Meta:
        abstract = True

    def can_serve_draft_versions(self, request):
        perms = request.user.get_all_permissions()
        if (
            request.user.is_superuser
            or getattr(request, "served_by_wagtail_sharing", False)
            or "regulations3k.change_section" in perms
        ):
            return True
        return False

    def get_versions_query(self, request):
        versions = self.regulation.versions

        if not self.can_serve_draft_versions(request):
            versions = versions.filter(draft=False)

        return versions

    def get_effective_version(self, request, date_str=None):
        """ Get the requested effective version if the user has permission """
        query_filter = {}

        if date_str is None:
            query_filter["effective_date__lte"] = date.today()
        else:
            query_filter["effective_date"] = date_str

        draft_permission = self.can_serve_draft_versions(request)
        if not draft_permission:
            query_filter["draft"] = False

        effective_version = (
            self.regulation.versions.filter(**query_filter)
            .order_by("-effective_date")
            .first()
        )

        if effective_version is None:
            raise Http404

        return effective_version

    def get_section_query(self, request=None, effective_version=None):
        """Query set for Sections in this regulation's effective version."""
        if effective_version is None:
            effective_version = self.get_effective_version(request)
        return Section.objects.filter(subpart__version=effective_version)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "regulation": self.regulation,
                "current_version": self.get_effective_version(request),
                "num_versions": self.get_versions_query(request).count(),
            }
        )
        return context

    def get_urls_for_version(self, effective_version, section=None):
        base_url = self.get_full_url()
        versions_url = urljoin(base_url, "versions") + "/"

        if effective_version.live_version:
            # This is the current version
            version_url = base_url
        else:
            # It's a past or future version, URLs have the date str
            date_str = str(effective_version.effective_date)
            version_url = urljoin(base_url, date_str) + "/"
            yield version_url

        if section is not None:
            yield urljoin(version_url, section.label) + "/"
        else:
            sections = self.get_section_query(
                effective_version=effective_version
            )
            yield version_url
            yield versions_url
            for section in sections.all():
                yield urljoin(version_url, section.label) + "/"

    def render_interp(self, context, raw_contents, **kwargs):
        # Extract the title from the raw regdown
        section_title_match = re.search(
            r"#+\s?(?P<section_title>.*)\s", raw_contents
        )
        if section_title_match is not None:
            context.update({"section_title": section_title_match.group(1)})
            span = section_title_match.span()
            raw_contents = (
                raw_contents[: span[0]] + raw_contents[span[1] :]  # noqa: E203
            )

        context.update({"contents": regdown(raw_contents)})
        context.update(kwargs)

        return get_template(self.interpretation_template).render(context)

    @route(r"^(?:(?P<date_str>[0-9]{4}-[0-9]{2}-[0-9]{2})/)?$", name="index")
    def index_route(self, request, date_str=None):
        request.is_preview = getattr(request, "is_preview", False)

        effective_version = self.get_effective_version(
            request, date_str=date_str
        )
        section_query = self.get_section_query(
            effective_version=effective_version
        )
        sections = list(section_query.all())

        context = self.get_context(request)
        context.update(
            {
                "requested_version": effective_version,
                "sections": sections,
                "get_secondary_nav_items": partial(
                    get_secondary_nav_items,
                    sections=sections,
                    date_str=date_str,
                ),
            }
        )

        if date_str is not None:
            context["date_str"] = date_str

        return TemplateResponse(request, self.template, context)

    @route(
        r"^versions/(?:(?P<section_label>[0-9A-Za-z-]+)/)?$", name="versions"
    )
    def versions_page(self, request, section_label=None):
        section_query = self.get_section_query(request=request)
        sections = list(section_query.all())
        context = self.get_context(request, sections=sections)

        versions = [
            {
                "effective_date": v.effective_date,
                "date_str": str(v.effective_date),
                "sections": self.get_section_query(effective_version=v).all(),
                "draft": v.draft,
            }
            for v in self.get_versions_query(request).order_by(
                "-effective_date"
            )
        ]

        context.update(
            {
                "versions": versions,
                "section_label": section_label,
                "get_secondary_nav_items": partial(
                    get_secondary_nav_items, sections=sections
                ),
            }
        )

        return TemplateResponse(request, self.versions_template, context)

    @route(
        r"^(?:(?P<date_str>[0-9]{4}-[0-9]{2}-[0-9]{2})/)?"
        r"(?P<section_label>[0-9A-Za-z-]+)/$",
        name="section",
    )
    def section_page(self, request, date_str=None, section_label=None):
        """ Render a section of the currently effective regulation """

        effective_version = self.get_effective_version(
            request, date_str=date_str
        )
        section_query = self.get_section_query(
            effective_version=effective_version
        )

        next_version = (
            self.get_versions_query(request)
            .filter(effective_date__gt=effective_version.effective_date)
            .first()
        )

        kwargs = {}
        if date_str is not None:
            kwargs["date_str"] = date_str

        try:
            section = section_query.get(label=section_label)
        except Section.DoesNotExist:
            return redirect(
                self.url + self.reverse_subpage("index", kwargs=kwargs)
            )

        sections = list(section_query.all())
        current_index = sections.index(section)
        context = self.get_context(
            request, section, sections=sections, **kwargs
        )

        content = regdown(
            section.contents,
            url_resolver=get_url_resolver(self, date_str=date_str),
            contents_resolver=get_contents_resolver(effective_version),
            render_block_reference=partial(self.render_interp, context),
        )

        next_section = get_next_section(sections, current_index)
        previous_section = get_previous_section(sections, current_index)

        context.update(
            {
                "requested_version": effective_version,
                "next_version": next_version,
                "section": section,
                "content": content,
                "get_secondary_nav_items": partial(
                    get_secondary_nav_items,
                    sections=sections,
                    date_str=date_str,
                ),
                "next_section": next_section,
                "next_url": get_section_url(
                    self, next_section, date_str=date_str
                ),
                "previous_section": previous_section,
                "previous_url": get_section_url(
                    self, previous_section, date_str=date_str
                ),
            }
        )

        return TemplateResponse(request, self.section_template, context)


class RegulationPage(RegulationPageMixin, Page):

    content_panels = Page.content_panels + RegulationPageMixin.content_panels
    template = "wagtailregulations/regulation_index.html"

    class Meta:
        abstract = True


def get_next_section(section_list, current_index):
    if current_index == len(section_list) - 1:
        return None
    else:
        return section_list[current_index + 1]


def get_previous_section(section_list, current_index):
    if current_index == 0:
        return None
    else:
        return section_list[current_index - 1]


def get_section_url(page, section, date_str=None):
    if section is None:
        return None

    section_kwargs = {}
    if date_str is not None:
        section_kwargs["date_str"] = date_str

    section_kwargs["section_label"] = section.label
    return page.url + page.reverse_subpage("section", kwargs=section_kwargs)


def get_secondary_nav_items(request, current_page, sections=[], date_str=None):
    url_bits = [bit for bit in request.path.split("/") if bit]
    current_label = url_bits[-1]
    subpart_dict = OrderedDict()

    section_kwargs = {}
    if date_str is not None:
        section_kwargs["date_str"] = date_str

    for section in sections:
        # If the section's subpart isn't in the subpart dict yet, add it
        if section.subpart not in subpart_dict:
            subpart_dict[section.subpart] = {"sections": [], "expanded": False}

        section_kwargs["section_label"] = section.label

        # Create the section dictionary for navigation
        section_dict = {
            "title": section.title,
            "url": get_section_url(current_page, section, date_str=date_str),
            "active": section.label == current_label,
            "expanded": True,
            "section": section,
        }

        # Add it to the subpart
        subpart_dict[section.subpart]["sections"].append(section_dict)

        # Set the subpart to active if the section is active
        if section_dict["active"]:
            subpart_dict[section.subpart]["expanded"] = True

    return subpart_dict, False
