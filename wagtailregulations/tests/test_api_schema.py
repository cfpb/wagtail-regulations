import json

from django.test import override_settings

from wagtail.core.models import Site

from graphene_django.utils.testing import GraphQLTestCase
from regulations_example.api.schema import schema
from regulations_example.models import (
    TestRegulationLandingPage,
    TestRegulationPage,
)
from wagtailregulations.tests.utils import RegulationsTestData


class SchemaTestCase(GraphQLTestCase, RegulationsTestData):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        super().setUp()
        self.setUp_regulations()

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

    def test_query_primary_fields(self):
        response = self.query(
            """
            query {
                regulations {
                    regulation {
                        cfrTitleNumber
                        chapter
                        partNumber
                        title
                        shortName
                        versions {
                            effectiveDate
                        }
                        effectiveVersion {
                            authority
                            source
                            effectiveDate
                            subparts {
                                label
                                title
                                sections {
                                    label
                                    title
                                    contents
                                    renderedContents
                                }
                            }
                        }
                    }
                }
            }
            """,
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        # Do some light introspection
        regulation_pages = content["data"]["regulations"]
        self.assertEqual(len(regulation_pages), 2)
        regulation = regulation_pages[0]["regulation"]
        self.assertEqual(len(regulation["versions"]), 2)
        self.assertEqual(regulation["partNumber"], self.part_1002.part_number)
        self.assertEqual(
            len(regulation["effectiveVersion"]["subparts"][0]["sections"]), 0
        )
        self.assertEqual(
            len(regulation["effectiveVersion"]["subparts"][1]["sections"]), 4
        )

    @override_settings(
        REGULATIONS_REFERENCE_MAPPING=[
            (
                r"(?P<label>(?P<section>[\w]+))-(?P<paragraph>[\w-]*-Interp)",
                "Interp-{section}",
                "{paragraph}",
            )
        ]
    )
    def test_query_rendered_contents(self):
        response = self.query(
            """
            query {
                regulations {
                    regulation {
                        effectiveVersion {
                            subparts {
                                sections  {
                                    label
                                    renderedContents
                                }
                            }
                        }
                    }
                }
            }
            """,
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        # Check to make sure the inline interp rendered with a blockquote
        regulation_pages = content["data"]["regulations"]
        regulation = regulation_pages[0]["regulation"]
        section = regulation["effectiveVersion"]["subparts"][1]["sections"][0]
        self.assertIn("blockquote", section["renderedContents"])
