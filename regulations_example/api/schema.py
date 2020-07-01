from wagtail.core.fields import StreamField

import graphene
from graphene.types import Scalar
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from regulations_example.models import TestRegulationPage
from wagtailregulations.api.schema import PartType


class GenericStreamFieldType(Scalar):
    @staticmethod
    def serialize(stream_value):
        return stream_value.stream_data


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return GenericStreamFieldType(
        description=field.help_text, required=not field.null
    )


class RegulationPageType(DjangoObjectType):
    regulation = graphene.Field(PartType)

    class Meta:
        model = TestRegulationPage
        fields = ("id", "slug", "body", "regulation")


class Query(graphene.ObjectType):
    regulation_pages = graphene.List(RegulationPageType)
    regulation_page = graphene.Field(
        RegulationPageType, id=graphene.Int(), slug=graphene.String()
    )

    def resolve_regulation_pages(self, info):
        return TestRegulationPage.objects.live()

    def resolve_regulation_page(self, info, id=None, slug=None):
        if id is not None:
            return TestRegulationPage.objects.live().get(id=id)
        if slug is not None:
            return TestRegulationPage.objects.live().get(slug=slug)


schema = graphene.Schema(query=Query)
