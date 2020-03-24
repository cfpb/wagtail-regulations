from regdown import regdown
from rest_framework import serializers
from wagtailregulations.models import EffectiveVersion, Part, Section, Subpart
from wagtailregulations.resolver import get_contents_resolver, get_url_resolver


class SectionSerializer(serializers.ModelSerializer):
    html_contents = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            "label",
            "subpart",
            "title",
            "contents",
            "html_contents",
        )

    def get_html_contents(self, section):
        effective_version = section.subpart.version
        date_str = str(effective_version.effective_date)
        page = section.subpart.version.part.page.first()
        html_contents = regdown(
            section.contents,
            url_resolver=get_url_resolver(page, date_str=date_str),
            contents_resolver=get_contents_resolver(effective_version),
        )
        return html_contents


class SubpartSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = Subpart
        fields = (
            "label",
            "title",
            "subpart_type",
            "version",
            "sections",
        )


class EffectiveVersionSerializer(serializers.ModelSerializer):
    subparts = SubpartSerializer(many=True)

    class Meta:
        model = EffectiveVersion
        fields = (
            "authority",
            "source",
            "effective_date",
            "part",
            "draft",
            "created",
            "subparts",
        )


class PartSerializer(serializers.ModelSerializer):
    versions = EffectiveVersionSerializer(many=True)

    class Meta:
        model = Part
        fields = (
            "cfr_title_number",
            "chapter",
            "part_number",
            "short_name",
            "chapter",
            "versions",
        )
