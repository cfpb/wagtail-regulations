# -*- coding: utf-8 -*-
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import FieldPanel


def sortable_label(label, separator="-"):
    """ Create a sortable tuple out of a label.
    Converts a dashed label into a tuple based on the following rules:
        - If a segment is numeric, it will get three leading zero places
        - If a segment is alphabetic and is already uppercase, it is
            returned as is.
        - If a segment is alphabetic but is not all uppercase, it is
            lowercased entirely.
        - Anything else is returned as-is.
    Intended to be used like `sorted(sections, key=Section.sortable_label)`
    """
    segments = []
    for segment in label.split(separator):
        if segment.isdigit():
            segments.append(segment.zfill(4))
        elif segment.isalpha() and segment.isupper():
            segments.append(segment)
        elif segment.isalpha():
            segments.append(segment.lower())
        else:
            segments.append(segment)
    return tuple(segments)


class Part(models.Model):
    cfr_title_number = models.CharField(max_length=255)
    chapter = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("cfr_title_number"),
        FieldPanel("title"),
        FieldPanel("part_number"),
        FieldPanel("short_name"),
        FieldPanel("chapter"),
    ]

    @property
    def cfr_title(self):
        return str(self)

    def __str__(self):
        name = "{} CFR Part {}".format(self.cfr_title_number, self.part_number)
        if self.short_name:
            name += " ({})".format(self.short_name)
        return name

    class Meta:
        ordering = ["part_number"]

    @cached_property
    def effective_version(self):
        """ Return the current effective version of the regulation.
        This selects based on effective_date being less than or equal to
        the current date and version is not a draft. """
        effective_version = (
            self.versions.filter(draft=False, effective_date__lte=date.today())
            .order_by("-effective_date")
            .first()
        )
        return effective_version


@python_2_unicode_compatible
class EffectiveVersion(models.Model):
    authority = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    effective_date = models.DateField(default=date.today)
    created = models.DateField(default=date.today)
    draft = models.BooleanField(default=False)
    part = models.ForeignKey(
        Part, related_name="versions", on_delete=models.CASCADE
    )

    panels = [
        FieldPanel("authority"),
        FieldPanel("source"),
        FieldPanel("effective_date"),
        FieldPanel("part"),
        FieldPanel("draft"),
        FieldPanel("created"),
    ]

    def __str__(self):
        return "Effective on {}".format(self.effective_date)

    @property
    def live_version(self):
        return self.part.effective_version == self

    @property
    def status(self):
        if self.live_version:
            return "LIVE"
        if self.draft is True:
            return "Unapproved draft"
        if self.effective_date >= date.today():
            return "Future version"
        return "Previous version"

    def validate_unique(self, exclude=None):
        super(EffectiveVersion, self).validate_unique(exclude=exclude)

        # Enforce some uniqueness on the effective-date. It will need to be
        # unique within a part, so if this part has a date the same as this
        # one, we throw a validation error.
        versions_with_this_date = self.part.versions.filter(
            effective_date=self.effective_date
        )

        if self.pk:
            versions_with_this_date = versions_with_this_date.exclude(
                pk=self.pk
            )

        if versions_with_this_date.count() > 0:
            raise ValidationError(
                {
                    "effective_date": [
                        "The part selected below already has an effective "
                        "version with this date."
                    ]
                }
            )

    class Meta:
        ordering = ["effective_date"]
        default_related_name = "version"


@python_2_unicode_compatible
class Subpart(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    version = models.ForeignKey(
        EffectiveVersion, related_name="subparts", on_delete=models.CASCADE
    )

    BODY = 0000
    APPENDIX = 1000
    INTERPRETATION = 2000
    SUBPART_TYPE_CHOICES = (
        (BODY, "Regulation Body"),
        (APPENDIX, "Appendix"),
        (INTERPRETATION, "Interpretation"),
    )
    subpart_type = models.IntegerField(
        choices=SUBPART_TYPE_CHOICES, default=BODY,
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("title"),
        FieldPanel("subpart_type"),
        FieldPanel("version"),
    ]

    def __str__(self):
        return self.title

    @property
    def subpart_heading(self):
        """Keeping for now as possible hook into secondary nav"""
        return ""

    @property
    def section_range(self):
        if self.subpart_type != Subpart.BODY or not self.sections.exists():
            return ""

        sections = self.sections.all()
        return "{}–{}".format(
            sections[0].numeric_label, sections.reverse()[0].numeric_label
        )

    class Meta:
        ordering = ["subpart_type", "label"]


@python_2_unicode_compatible
class Section(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    contents = models.TextField(blank=True)
    subpart = models.ForeignKey(
        Subpart, related_name="sections", on_delete=models.CASCADE
    )
    sortable_label = models.CharField(max_length=255)

    panels = [
        FieldPanel("label"),
        FieldPanel("subpart"),
        FieldPanel("title"),
        FieldPanel("contents"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["sortable_label"]

    def save(self, **kwargs):
        self.sortable_label = "-".join(sortable_label(self.label))
        super(Section, self).save(**kwargs)

    @cached_property
    def part(self):
        return self.subpart.version.part.part_number

    @property
    def section_number(self):
        return self.label

    @property
    def numeric_label(self):
        if self.label.isdigit():
            return "\xa7\xa0{}.{}".format(self.part, int(self.label))
        else:
            return ""

    @property
    def title_content(self):
        if self.numeric_label:
            return self.title.replace(self.numeric_label, "").strip()
        else:
            return self.title
