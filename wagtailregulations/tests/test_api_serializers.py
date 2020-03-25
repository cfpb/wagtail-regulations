from wagtail.core.models import Site

from regulations_example.models import (
    TestRegulationLandingPage,
    TestRegulationPage,
)
from wagtailregulations.api.serializers import (
    EffectiveVersionSerializer,
    PartSerializer,
    SectionSerializer,
    SubpartSerializer,
)
from wagtailregulations.tests.utils import RegulationsTestCase


class SerializersTestCase(RegulationsTestCase):
    def setUp(self):
        super().setUp()

        self.site = Site.objects.get(is_default_site=True)

        self.landing_page = TestRegulationLandingPage(
            title="Regulations", slug="reg-landing"
        )
        self.site.root_page.add_child(instance=self.landing_page)
        self.landing_page.save_revision().publish()

        self.reg_page = TestRegulationPage(
            regulation=self.part_1002, title="Reg B", slug="1002"
        )
        self.landing_page.add_child(instance=self.reg_page)
        self.reg_page.save_revision().publish()

        self.reg_page_1030 = TestRegulationPage(
            regulation=self.part_1030, title="Reg C", slug="1030"
        )
        self.landing_page.add_child(instance=self.reg_page_1030)
        self.reg_page_1030.save_revision()

    def test_section_serialier(self):
        data = SectionSerializer(self.section_num4).data
        self.assertIn("html_contents", data)

    def test_subpart_serialier(self):
        data = SubpartSerializer(self.subpart).data
        self.assertIn("sections", data)

    def test_effective_version_serializer(self):
        data = EffectiveVersionSerializer(self.effective_version).data
        self.assertIn("subparts", data)

    def test_part_serializer(self):
        data = PartSerializer(self.part_1002).data
        self.assertIn("versions", data)
