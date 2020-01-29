from rest_framework import relations, serializers

from wagtailregulations.models import Part, EffectiveVersion, Subpart, Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            'label',
            'subpart',
            'title',
            'contents',
        )


class SubpartSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = Subpart
        fields = (
            'label',
            'title',
            'subpart_type',
            'version',
            'sections',
        )


class EffectiveVersionSerializer(serializers.ModelSerializer):
    subparts = SubpartSerializer(many=True)

    class Meta:
        model = EffectiveVersion
        fields = (
            'authority',
            'source',
            'effective_date',
            'part',
            'draft',
            'created',
            'subparts',
        )


class PartSerializer(serializers.ModelSerializer):
    versions = EffectiveVersionSerializer(many=True)

    class Meta:
        model = Part
        fields = (
            'cfr_title_number',
            'chapter',
            'part_number',
            'short_name',
            'chapter',
            'versions',
        )
