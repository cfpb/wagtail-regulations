from wagtailregulations.blocks import BaseRegulationsList
from wagtailregulations.models import RegulationPage

import wagtail


if wagtail.VERSION >= (2, 0):
    from wagtail.contrib.routable_page.models import RoutablePage
    from wagtail.admin.edit_handlers import StreamFieldPanel
    from wagtail.core import blocks
    from wagtail.core.fields import StreamField
else:
    from wagtail.contrib.wagtailroutablepage.models import RoutablePage
    from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
    from wagtail.wagtailcore import blocks
    from wagtail.wagtailcore.fields import StreamField


class TestRegulationLandingPage(RoutablePage):
    body = StreamField([
        ('title', blocks.CharBlock()),
        ('introduction', blocks.RichTextBlock()),
        ('regulations_list', BaseRegulationsList(
            'regulations_example.TestRegulationPage'
        )),
    ])

    content_panels = RoutablePage.content_panels + [
        StreamFieldPanel('body'),
    ]


class TestRegulationPage(RegulationPage):
    """A routable page for serving an eregulations page by Section ID."""

    subpage_types = []

    body = StreamField([
        ('title', blocks.CharBlock()),
        ('introduction', blocks.RichTextBlock()),
    ])

    content_panels = RegulationPage.content_panels + [
        StreamFieldPanel('body'),
    ]
