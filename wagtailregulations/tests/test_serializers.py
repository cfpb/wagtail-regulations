from wagtailregulations.serializers import (
    SectionSerializer,
    SubpartSerializer,
    EffectiveVersionSerializer,
    PartSerializer,
)
from wagtailregulations.tests.utils import RegulationsTestCase


try:
    from wagtail.core.models import Site
except ImportError:
    from wagtail.wagtailcore.models import Site


class SerializersTestCase(RegulationsTestCase):

    def test_subpart_serialier(self):
        data = SubpartSerializer(self.subpart).data
        self.assertIn('sections', data)

    def test_effective_version_serializer(self):
        data = EffectiveVersionSerializer(self.effective_version).data
        self.assertIn('subparts', data)

    def test_part_serializer(self):
        data = PartSerializer(self.part_1002).data
        self.assertIn('versions', data)
