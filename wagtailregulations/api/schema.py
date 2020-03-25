import graphene
from graphene_django import DjangoObjectType
from regdown import regdown
from wagtailregulations.models import EffectiveVersion, Part, Section, Subpart
from wagtailregulations.resolver import get_contents_resolver, get_url_resolver


class SectionNode(DjangoObjectType):
    class Meta:
        model = Section
        fields = (
            "label",
            "title",
            "contents",
            "rendered_contents",
        )

    rendered_contents = graphene.String()

    def resolve_rendered_contents(self, info):
        effective_version = self.subpart.version
        date_str = str(effective_version.effective_date)
        page = self.subpart.version.part.page.first()
        html_contents = regdown(
            self.contents,
            url_resolver=get_url_resolver(page, date_str=date_str),
            contents_resolver=get_contents_resolver(effective_version),
        )
        return html_contents


class SubpartNode(DjangoObjectType):
    class Meta:
        model = Subpart
        fields = (
            "label",
            "title",
            "sections",
        )


class EffectiveVersionNode(DjangoObjectType):
    class Meta:
        model = EffectiveVersion
        fields = (
            "authority",
            "source",
            "effective_date",
            "subparts",
        )


class PartNode(DjangoObjectType):
    class Meta:
        model = Part
        fields = (
            "cfr_title_number",
            "chapter",
            "part_number",
            "title",
            "short_name",
            "versions",
        )

    effective_version = graphene.Field(EffectiveVersionNode)

    def resolve_effective_version(self, info):
        return self.effective_version

    def resolve_versions(self, info):
        return self.versions.filter(draft=False)
