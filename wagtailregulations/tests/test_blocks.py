from wagtail.core.models import Page, Site

from regulations_example.models import (
    TestRegulationLandingPage,
    TestRegulationPage,
)
from wagtailregulations.blocks import BaseRegulationsList
from wagtailregulations.tests.utils import RegulationsTestCase


class RegulationsListTestCase(RegulationsTestCase):
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
            regulation=self.part_1030, title="Reg C", slug="1030", live=False,
        )
        self.landing_page.add_child(instance=self.reg_page_1030)
        self.reg_page_1030.save_revision()

        self.more_regs_page = Page.objects.first()

    def test_regulations_list_invalid_model(self):
        pass

    def test_regulations_list_has_regs(self):
        block = BaseRegulationsList("regulations_example.TestRegulationPage")
        result = block.render(
            block.to_python({"more_regs_page": self.more_regs_page.pk})
        )
        self.assertIn("Reg B", result)
        self.assertIn("/1002/", result)
        # self.assertIn('New amendments effective', result)
        self.assertNotIn("Reg C", result)
        self.assertNotIn("/1030/", result)
