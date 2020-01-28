from datetime import date

from django.db.models import Prefetch
from django.apps import apps

from wagtail.wagtailcore import blocks

from wagtailregulations.models.django import EffectiveVersion


class BaseRegulationsList(blocks.StructBlock):
    ordering = 'title'

    def __init__(self, model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def get_ordering(self, value):
        return self.ordering

    def filter_queryset(self, qs, value):
        return qs.live()

    def get_queryset(self, value):
        model_cls = apps.get_model(self.model)
        qs = model_cls.objects.all()
        qs = self.filter_queryset(qs, value)
        ordering = self.get_ordering(value)

        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)

            qs = qs.order_by(*ordering)

        future_versions_qs = EffectiveVersion.objects.filter(
            draft=False,
            effective_date__gte=date.today()
        )
        qs = qs.prefetch_related(
            Prefetch(
                'regulation__versions',
                queryset=future_versions_qs,
                to_attr='future_versions'
            )
        )
        return qs

    def get_context(self, value, parent_context=None):
        context = super().get_context(
            value, parent_context=parent_context
        )
        context['regulations'] = self.get_queryset(value)
        return context

    class Meta:
        icon = 'list-ul'
        template = 'wagtailregulations/regulations-listing.html'
