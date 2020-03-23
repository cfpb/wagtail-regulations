import datetime
import unittest

# from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser, User
from django.http import Http404
from django.test import RequestFactory

from wagtail.core.models import Site

from regulations_example.models import (
    TestRegulationLandingPage,
    TestRegulationPage,
)
from wagtailregulations.models.django import Subpart
from wagtailregulations.models.pages import (
    get_next_section,
    get_previous_section,
    get_secondary_nav_items,
    get_section_url,
)
from wagtailregulations.tests.utils import RegulationsTestCase


class RegModelTests(RegulationsTestCase):
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

        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(
            username="supertest", password="test", email="test@email.com"
        )

    def get_request(self, path="", data={}):
        request = self.factory.get(path, data=data)
        request.site = self.site
        request.user = AnonymousUser()
        return request

    def test_routable_reg_page_get_context(self):
        test_context = self.reg_page.get_context(self.get_request())
        self.assertEqual(test_context["regulation"], self.reg_page.regulation)

    def test_get_secondary_nav_items(self):
        request = self.get_request()
        request.path = "/regulations/1002/4/"
        sections = list(self.reg_page.get_section_query(request).all())
        test_nav_items = get_secondary_nav_items(
            request, self.reg_page, sections
        )[0]
        self.assertEqual(
            len(test_nav_items),
            Subpart.objects.filter(version=self.effective_version)
            .exclude(sections=None)
            .count(),
        )

    def test_get_section_url(self):
        url = get_section_url(self.reg_page, self.section_num4)
        self.assertEqual(url, "/reg-landing/1002/4/")

    def test_get_section_url_no_section(self):
        url = get_section_url(self.reg_page, None)
        self.assertIsNone(url)

    def test_section_page_view(self):
        response = self.client.get("/reg-landing/1002/4/")
        self.assertEqual(response.status_code, 200)

    def test_section_page_view_section_does_not_exist(self):
        response = self.client.get("/reg-landing/1002/82/")
        self.assertRedirects(
            response, "/reg-landing/1002/", fetch_redirect_response=False
        )

    def test_section_page_view_section_does_not_exist_with_date(self):
        response = self.client.get("/reg-landing/1002/2011-01-01/82/")
        self.assertRedirects(
            response,
            "/reg-landing/1002/2011-01-01/",
            fetch_redirect_response=False,
        )

    def test_render_interp(self):
        result = self.reg_page.render_interp({}, "some contents")
        self.assertIn("some contents", result)

    def test_render_interp_with_title(self):
        result = self.reg_page.render_interp({}, "# A title\n\nsome contents")
        self.assertIn("Official interpretation of A title", result)
        self.assertIn("some contents", result)

    def test_get_effective_version_not_draft(self):
        request = self.get_request()
        effective_version = self.reg_page.get_effective_version(
            request, "2014-01-18"
        )
        self.assertEqual(effective_version, self.effective_version)

    def test_get_effective_version_draft_with_perm(self):
        request = self.get_request()
        request.user = self.superuser
        effective_version = self.reg_page.get_effective_version(
            request, "2020-01-01"
        )
        self.assertEqual(effective_version, self.draft_effective_version)

    def test_get_effective_version_draft_without_perm(self):
        request = self.get_request()
        with self.assertRaises(Http404):
            self.reg_page.get_effective_version(request, "2020-01-01")

    def test_get_effective_version_dne(self):
        request = self.get_request()
        with self.assertRaises(Http404):
            self.reg_page.get_effective_version(request, "2050-01-01")

    def test_index_page_with_effective_date(self):
        response = self.client.get("/reg-landing/1002/2011-01-01/")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            response.context_data["current_version"],
            response.context_data["requested_version"],
        )
        self.assertEqual(
            response.context_data["requested_version"].effective_date,
            datetime.date(2011, 1, 1),
        )

    def test_index_page_without_effective_date(self):
        response = self.client.get("/reg-landing/1002/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data["current_version"].effective_date,
            datetime.date(2014, 1, 18),
        )

    def test_section_page_with_effective_date(self):
        response = self.client.get("/reg-landing/1002/2011-01-01/4/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"This version is not the current regulation", response.content
        )

    def test_section_page_without_effective_date(self):
        response = self.client.get("/reg-landing/1002/4/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"This version is the current regulation", response.content
        )

    def test_versions_page_view_without_section(self):
        response = self.client.get("/reg-landing/1002/versions/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jan. 18, 2014", response.content)
        self.assertIn(b"(current regulation)", response.content)
        self.assertIn(b"Jan. 1, 2011", response.content)
        self.assertNotIn(b"Jan. 1, 2020", response.content)

    def test_versions_page_view_with_section(self):
        response = self.client.get("/reg-landing/1002/versions/4/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'href="/reg-landing/1002/2011-01-01/4/"', response.content
        )

    def test_get_urls_for_version(self):
        urls = list(self.reg_page.get_urls_for_version(self.effective_version))
        self.assertIn("http://localhost/reg-landing/1002/", urls)
        self.assertIn("http://localhost/reg-landing/1002/4/", urls)
        self.assertIn("http://localhost/reg-landing/1002/versions/", urls)

        urls = list(
            self.reg_page.get_urls_for_version(
                self.effective_version, section=self.section_num4
            )
        )
        self.assertEqual(["http://localhost/reg-landing/1002/4/"], urls)

        urls = list(
            self.reg_page.get_urls_for_version(self.old_effective_version)
        )
        self.assertIn("http://localhost/reg-landing/1002/2011-01-01/", urls)
        self.assertIn("http://localhost/reg-landing/1002/2011-01-01/4/", urls)

    def test_reg_page_can_serve_draft_versions(self):
        request = self.get_request()
        request.served_by_wagtail_sharing = True
        self.assertTrue(self.reg_page.can_serve_draft_versions(request))

    def test_reg_page_num_versions_on_sharing(self):
        request = self.get_request()
        request.served_by_wagtail_sharing = True
        test_context = self.reg_page.get_context(request)
        self.assertEqual(test_context["num_versions"], 3)

    def test_reg_page_num_versions_off_sharing(self):
        test_context = self.reg_page.get_context(self.get_request())
        self.assertEqual(test_context["num_versions"], 2)

    def test_reg_page_next_version_none(self):
        response = self.client.get("/reg-landing/1002/4/")
        self.assertIsNone(response.context_data["next_version"])

    def test_reg_page_next_version(self):
        response = self.client.get("/reg-landing/1002/2011-01-01/4/")
        self.assertEqual(
            response.context_data["next_version"], self.effective_version
        )


class SectionNavTests(unittest.TestCase):
    def test_get_next_section(self):
        section_list = ["1002.1", "1002.2"]
        current_index = 0
        self.assertEqual(
            get_next_section(section_list, current_index), "1002.2"
        )

    def test_get_next_section_none(self):
        section_list = ["1002.1", "1002.2"]
        current_index = 1
        self.assertIs(get_next_section(section_list, current_index), None)

    def test_get_previous_section(self):
        section_list = ["1002.1", "1002.2"]
        current_index = 1
        self.assertEqual(
            get_previous_section(section_list, current_index), "1002.1"
        )

    def test_get_previous_section_none(self):
        section_list = ["1002.1", "1002.2"]
        current_index = 0
        self.assertIs(get_previous_section(section_list, current_index), None)
