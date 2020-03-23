# -*- coding: utf-8 -*-
import sys
from datetime import date, datetime, timedelta

from django.core.exceptions import ValidationError

from model_mommy import mommy
from wagtailregulations.models.django import (
    EffectiveVersion,
    Subpart,
    sortable_label,
)
from wagtailregulations.tests.utils import RegulationsTestCase


class RegModelTests(RegulationsTestCase):
    def test_part_string_method(self):
        self.assertEqual(
            self.part_1002.__str__(), "12 CFR Part 1002 (Regulation B)"
        )

    def test_part_cfr_title_method(self):
        part = self.part_1002
        self.assertEqual(
            part.cfr_title,
            "{} CFR Part {} ({})".format(
                part.cfr_title_number, part.part_number, part.short_name
            ),
        )

    def test_subpart_string_method(self):
        self.assertEqual(self.subpart.__str__(), "Subpart A - General")

    def test_section_string_method(self):
        if sys.version_info >= (3, 0):  # pragma: no cover
            self.assertEqual(
                self.section_num4.__str__(), "\xa7\xa01002.4 General rules."
            )
        else:  # pragma: no cover
            self.assertEqual(
                self.section_num4.__str__(),
                "\xa7\xa01002.4 General rules.".encode("utf8"),
            )

    def test_subpart_headings(self):
        for each in Subpart.objects.all():
            self.assertEqual(each.subpart_heading, "")

    def test_effective_version_string_method(self):
        self.assertEqual(
            self.effective_version.__str__(), "Effective on 2014-01-18"
        )

    def test_live_version_true(self):
        self.assertTrue(self.effective_version.live_version)

    def test_status_is_live(self):
        self.assertEqual(self.effective_version.status, "LIVE")

    def test_status_is_draft(self):
        today_plus_five = datetime.today().date() + timedelta(days=5)

        self.effective_version.draft = True
        self.effective_version.save()
        self.assertEqual(self.effective_version.status, "Unapproved draft")
        self.effective_version.draft = False
        self.effective_version.effective_date = today_plus_five

        self.effective_version.save()
        self.assertEqual(self.effective_version.status, "Future version")
        self.effective_version.effective_date = date(2014, 1, 18)
        self.effective_version.save()

    def test_status_is_previous_version(self):
        self.assertEqual(self.old_effective_version.status, "Previous version")

    def test_sortable_label(self):
        self.assertEqual(
            sortable_label("1-A-Interp-√"), ("0001", "A", "interp", "√")
        )

    def test_section_ranges(self):
        self.assertEqual(self.subpart_orphan.section_range, "")
        self.assertEqual(self.subpart_appendices.section_range, "")
        self.assertEqual(self.subpart_interps.section_range, "")
        self.assertEqual(
            self.subpart.section_range, "\xa7\xa01002.2\u2013\xa7\xa01002.15"
        )

    def test_section_title_content(self):
        self.assertEqual(
            self.section_num15.title_content,
            "Rules concerning requests for information.",
        )

    def test_section_part(self):
        self.assertEqual(self.section_num4.part, "1002")

    def test_section_section_number(self):
        self.assertEqual(self.section_num4.section_number, "4")

    def test_section_numeric_label(self):
        self.assertEqual(self.section_num4.numeric_label, "\xa7\xa01002.4")

    def test_section_numeric_label_not_digits(self):
        self.assertEqual(self.section_alpha.numeric_label, "")

    def test_section_title_content_not_digits(self):
        self.assertEqual(
            self.section_beta.title_content, "Appendix B to Part 1002-Errata"
        )

    def test_effective_version_date_unique(self):
        new_effective_version = mommy.make(
            EffectiveVersion,
            effective_date=date(2020, 1, 1),
            part=self.part_1002,
            draft=True,
        )
        with self.assertRaises(ValidationError):
            new_effective_version.validate_unique()
