import datetime

from django.test import TestCase

from model_mommy import mommy
from wagtailregulations.models.django import (
    EffectiveVersion,
    Part,
    Section,
    Subpart,
)


class RegulationsTestData(object):
    def setUp_regulations(self):
        self.part_1002 = mommy.make(
            Part,
            cfr_title_number="12",
            part_number="1002",
            title="Equal Credit Opportunity Act",
            short_name="Regulation B",
            chapter="X",
        )
        self.part_1030 = mommy.make(
            Part,
            part_number="1030",
            title="Truth In Savings",
            short_name="Regulation DD",
            chapter="X",
        )
        self.effective_version = mommy.make(
            EffectiveVersion,
            effective_date=datetime.date(2014, 1, 18),
            part=self.part_1002,
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
            label="Subpart General",
            title="Subpart A - General",
            subpart_type=Subpart.BODY,
            version=self.effective_version,
        )
        self.subpart_appendices = mommy.make(
            Subpart,
            label="Appendices",
            title="Appendices",
            subpart_type=Subpart.APPENDIX,
            version=self.effective_version,
        )
        self.subpart_interps = mommy.make(
            Subpart,
            label="Official Interpretations",
            title="Supplement I to Part 1002",
            subpart_type=Subpart.INTERPRETATION,
            version=self.effective_version,
        )
        self.subpart_orphan = mommy.make(
            Subpart,
            label="General Mistake",
            title="An orphan subpart with no sections for testing",
            version=self.effective_version,
        )
        self.old_subpart = mommy.make(
            Subpart,
            label="Subpart General",
            title="General",
            subpart_type=Subpart.BODY,
            version=self.old_effective_version,
        )
        self.section_num2 = mommy.make(
            Section,
            label="2",
            title="\xa7 1002.2 Definitions.",
            contents="{c}\nAdverse action.\n\nsee(2-c-Interp)\n",
            subpart=self.subpart,
        )
        self.section_num3 = mommy.make(
            Section,
            label="3",
            title="\xa7 1002.3 Limited exceptions.",
            contents="{b}\nSecurities credit.\n\nsee(3-b-Interp)\n",
            subpart=self.subpart,
        )
        self.section_num4 = mommy.make(
            Section,
            label="4",
            title="\xa7\xa01002.4 General rules.",
            contents=(
                "{a}\n(a) Regdown paragraph a.\n"
                "{b}\n(b) Paragraph b\n"
                "\nsee(4-b-Interp)\n"
                "{c}\n(c) Paragraph c.\n"
                "{c-1}\n \n"
                "{d}\n(1) General rule. A creditor that provides in writing.\n"
            ),
            subpart=self.subpart,
        )
        self.section_num15 = mommy.make(
            Section,
            label="15",
            title="\xa7\xa01002.15 Rules concerning requests for information.",
            contents="regdown content.",
            subpart=self.subpart,
        )
        self.section_alpha = mommy.make(
            Section,
            label="A",
            title=(
                "Appendix A to Part 1002-Federal Agencies "
                "To Be Listed in Adverse Action Notices"
            ),
            contents="regdown content.",
            subpart=self.subpart_appendices,
        )
        self.section_beta = mommy.make(
            Section,
            label="B",
            title=("Appendix B to Part 1002-Errata"),
            contents="regdown content.",
            subpart=self.subpart_appendices,
        )
        self.section_interps = mommy.make(
            Section,
            label="Interp-A",
            title=("Official interpretations for Appendix A to Part 1002"),
            contents="interp content.",
            subpart=self.subpart_interps,
        )
        self.old_section_num4 = mommy.make(
            Section,
            label="4",
            title="\xa7\xa01002.4 General rules.",
            contents="regdown contents",
            subpart=self.old_subpart,
        )
        self.section_interp2 = mommy.make(
            Section,
            label="Interp-2",
            title="Section 1002.2—Definitions",
            contents="{c-Interp}\nInterpreting adverse action\n\n",
            subpart=self.subpart_interps,
        )


class RegulationsTestCase(TestCase, RegulationsTestData):
    def setUp(self):
        self.setUp_regulations()
