from __future__ import unicode_literals

import datetime
import sys

# from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy
from wagtailregulations.models.django import (
    EffectiveVersion,
    Part,
    Section,
    Subpart,
    sortable_label,
)


class RegModelTests(TestCase):

    def setUp(self):
        self.part_1002 = mommy.make(
            Part,
            part_number='1002',
            title='Equal Credit Opportunity Act',
            letter_code='B',
            chapter='X'
        )
        self.part_1030 = mommy.make(
            Part,
            part_number='1030',
            title='Truth In Savings',
            letter_code='DD', chapter='X'
        )
        self.effective_version = mommy.make(
            EffectiveVersion,
            effective_date=datetime.date(2014, 1, 18),
            part=self.part_1002
        )
        self.old_effective_version = mommy.make(
            EffectiveVersion,
            effective_date=datetime.date(2011, 1, 1),
            part=self.part_1002,
        )
        self.draft_effective_version = mommy.make(
            EffectiveVersion,
            effective_date=datetime.date(2020, 1, 1),
            part=self.part_1002,
            draft=True,
        )
        self.subpart = mommy.make(
            Subpart,
            label='Subpart General',
            title='Subpart A - General',
            subpart_type=Subpart.BODY,
            version=self.effective_version
        )
        self.subpart_appendices = mommy.make(
            Subpart,
            label='Appendices',
            title='Appendices',
            subpart_type=Subpart.APPENDIX,
            version=self.effective_version
        )
        self.subpart_interps = mommy.make(
            Subpart,
            label='Official Interpretations',
            title='Supplement I to Part 1002',
            subpart_type=Subpart.INTERPRETATION,
            version=self.effective_version
        )
        self.subpart_orphan = mommy.make(
            Subpart,
            label='General Mistake',
            title='An orphan subpart with no sections for testing',
            version=self.effective_version
        )
        self.old_subpart = mommy.make(
            Subpart,
            label='Subpart General',
            title='General',
            subpart_type=Subpart.BODY,
            version=self.old_effective_version
        )
        self.section_num4 = mommy.make(
            Section,
            label='4',
            title='\xa7\xa01002.4 General rules.',
            contents=(
                '{a}\n(a) Regdown paragraph a.\n'
                '{b}\n(b) Paragraph b\n'
                '\nsee(4-b-Interp)\n'
                '{c}\n(c) Paragraph c.\n'
                '{c-1}\n \n'
                '{d}\n(1) General rule. A creditor that provides in writing.\n'
            ),
            subpart=self.subpart,
        )
        self.section_num15 = mommy.make(
            Section,
            label='15',
            title='\xa7\xa01002.15 Rules concerning requests for information.',
            contents='regdown content.',
            subpart=self.subpart,
        )
        self.section_alpha = mommy.make(
            Section,
            label='A',
            title=('Appendix A to Part 1002-Federal Agencies '
                   'To Be Listed in Adverse Action Notices'),
            contents='regdown content.',
            subpart=self.subpart_appendices,
        )
        self.section_beta = mommy.make(
            Section,
            label='B',
            title=('Appendix B to Part 1002-Errata'),
            contents='regdown content.',
            subpart=self.subpart_appendices,
        )
        self.section_interps = mommy.make(
            Section,
            label='Interp-A',
            title=('Official interpretations for Appendix A to Part 1002'),
            contents='interp content.',
            subpart=self.subpart_interps,
        )
        self.old_section_num4 = mommy.make(
            Section,
            label='4',
            title='\xa7\xa01002.4 General rules.',
            contents='regdown contents',
            subpart=self.old_subpart,
        )

    def test_part_string_method(self):
        self.assertEqual(
            self.part_1002.__str__(),
            '12 CFR Part 1002 (Regulation B)'
        )

    def test_part_cfr_title_method(self):
        part = self.part_1002
        self.assertEqual(
            part.cfr_title,
            "{} CFR Part {} (Regulation {})".format(
                part.cfr_title_number,
                part.part_number,
                part.letter_code))

    def test_subpart_string_method(self):
        self.assertEqual(
            self.subpart.__str__(),
            'Subpart A - General')

    def test_section_string_method(self):
        if sys.version_info >= (3, 0):  # pragma: no cover
            self.assertEqual(
                self.section_num4.__str__(),
                '\xa7\xa01002.4 General rules.')
        else:  # pragma: no cover
            self.assertEqual(
                self.section_num4.__str__(),
                '\xa7\xa01002.4 General rules.'.encode('utf8'))

    def test_section_export_graphs(self):
        test_counts = self.section_num4.extract_graphs()
        self.assertEqual(test_counts['section'], "1002-4")
        self.assertEqual(test_counts['created'], 4)
        self.assertEqual(test_counts['deleted'], 1)
        self.assertEqual(test_counts['kept'], 1)

    def test_section_paragraph_str(self):
        self.assertEqual(
            self.graph_to_keep.__str__(),
            "Section 1002-4 paragraph d")

    def test_subpart_headings(self):
        for each in Subpart.objects.all():
            self.assertEqual(each.subpart_heading, '')

    def test_effective_version_string_method(self):
        self.assertEqual(
            self.effective_version.__str__(),
            'Effective on 2014-01-18')

    def test_live_version_true(self):
        self.assertTrue(self.effective_version.live_version)

    def test_status_is_live(self):
        self.assertEqual(self.effective_version.status, 'LIVE')

    def test_status_is_draft(self):
        self.effective_version.draft = True
        self.effective_version.save()
        self.assertEqual(self.effective_version.status, 'Unapproved draft')
        self.effective_version.draft = False
        self.effective_version.effective_date = (
            datetime.datetime.today().date() + datetime.timedelta(days=5))
        self.effective_version.save()
        self.assertEqual(self.effective_version.status, 'Future version')
        self.effective_version.effective_date = datetime.date(2014, 1, 18)
        self.effective_version.save()

    def test_status_is_previous_version(self):
        self.assertEqual(self.old_effective_version.status, 'Previous version')

    def test_sortable_label(self):
        self.assertEqual(
            sortable_label('1-A-Interp'),
            ('0001', 'A', 'interp')
        )

    def test_section_ranges(self):
        self.assertEqual(self.subpart_orphan.section_range, '')
        self.assertEqual(self.subpart_appendices.section_range, '')
        self.assertEqual(self.subpart_interps.section_range, '')
        self.assertEqual(
            self.subpart.section_range,
            '\xa7\xa01002.4\u2013\xa7\xa01002.15')

    def test_section_title_content(self):
        self.assertEqual(
            self.section_num15.title_content,
            'Rules concerning requests for information.')

    def test_section_part(self):
        self.assertEqual(self.section_num4.part, '1002')

    def test_section_section_number(self):
        self.assertEqual(self.section_num4.section_number, '4')

    def test_section_numeric_label(self):
        self.assertEqual(self.section_num4.numeric_label, '\xa7\xa01002.4')

    def test_section_numeric_label_not_digits(self):
        self.assertEqual(self.section_alpha.numeric_label, '')

    def test_section_title_content_not_digits(self):
        self.assertEqual(
            self.section_beta.title_content,
            'Appendix B to Part 1002-Errata'
        )

    def test_effective_version_date_unique(self):
        new_effective_version = mommy.make(
            EffectiveVersion,
            effective_date=datetime.date(2020, 1, 1),
            part=self.part_1002,
            draft=True,
        )
        with self.assertRaises(ValidationError):
            new_effective_version.validate_unique()
