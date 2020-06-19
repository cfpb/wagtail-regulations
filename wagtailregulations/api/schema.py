import graphene
from graphene_django import DjangoObjectType
from regdown import regdown
from wagtailregulations.models import EffectiveVersion, Part, Section, Subpart
from wagtailregulations.resolver import get_contents_resolver, get_url_resolver


class SectionType(DjangoObjectType):
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


class SubpartType(DjangoObjectType):
    class Meta:
        model = Subpart
        fields = (
            "label",
            "title",
            "sections",
        )

    section = graphene.Field(SectionType, label=graphene.String())

    def resolve_section(self, info, label=None):
        if label is not None:
            return Section.objects.get(label=label, subpart=self)


class EffectiveVersionType(DjangoObjectType):
    class Meta:
        model = EffectiveVersion
        fields = (
            "authority",
            "source",
            "effective_date",
            "subparts",
        )

    subpart = graphene.Field(SubpartType, label=graphene.String())

    def resolve_subpart(self, info, label=None):
        if label is not None:
            return Subpart.objects.get(label=label, version=self)


class PartType(DjangoObjectType):
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

    effective_version = graphene.Field(EffectiveVersionType)
    version = graphene.Field(
        EffectiveVersionType, effective_date=graphene.Date()
    )

    def resolve_effective_version(self, info):
        return self.effective_version

    def resolve_versions(self, info):
        return self.versions.filter(draft=False)

    def resolve_version(self, info, effective_date=None):
        if effective_date is not None:
            return EffectiveVersion.objects.get(
                effective_date=effective_date, part=self
            )
