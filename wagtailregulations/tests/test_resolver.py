# -*- coding: utf-8 -*-
from django.test import override_settings

from wagtail.core.models import Site

from regdown import DEFAULT_RENDER_BLOCK_REFERENCE, regdown
from regulations_example.models import (
    TestRegulationLandingPage,
    TestRegulationPage,
)
from wagtailregulations.resolver import (
    get_contents_resolver,
    get_url_resolver,
    resolve_reference,
)
from wagtailregulations.tests.utils import RegulationsTestCase


# Our setup and tests use as close to regulation examples as possible.
# Override the default settings to let us map old-eRegs-style labels to new
# Regulations3k sections and paragraphs.
@override_settings(
    REGULATIONS_REFERENCE_MAPPING=[
        (
            r"(?P<label>(?P<section>[\w]+))-(?P<paragraph>[\w-]*-Interp)",
            "Interp-{section}",
            "{paragraph}",
        )
    ]
)
class ReferenceResolutionTestCase(RegulationsTestCase):
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

    def test_resolve_reference(self):
        section, paragraph = resolve_reference("2-c-Interp")
        self.assertEqual(section, "Interp-2")
        self.assertEqual(paragraph, "c-Interp")

    def test_resolve_reference_no_match(self):
        section, paragraph = resolve_reference("foo")
        self.assertIsNone(section)
        self.assertIsNone(paragraph)

    def test_get_contents_resolver(self):
        contents_resolver = get_contents_resolver(
            self.reg_page.regulation.effective_version
        )
        result = regdown(
            self.section_num2.contents,
            contents_resolver=contents_resolver,
            render_block_reference=DEFAULT_RENDER_BLOCK_REFERENCE,
        )
        self.assertIn("Interpreting adverse action", result)

    def test_get_contents_resolver_reference_doesnt_exist(self):
        contents_resolver = get_contents_resolver(
            self.reg_page.regulation.effective_version
        )
        result = regdown(
            self.section_num3.contents,
            contents_resolver=contents_resolver,
            render_block_reference=DEFAULT_RENDER_BLOCK_REFERENCE,
        )
        self.assertEqual(
            result,
            '<p class="regdown-block level-0" data-label="b" id="b">'
            "Securities credit.</p>",
        )

    def test_get_url_resolver(self):
        url_resolver = get_url_resolver(self.reg_page)
        result = url_resolver("2-c-Interp")
        self.assertEqual(result, "/reg-landing/1002/Interp-2/#c-Interp")
