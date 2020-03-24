from django.conf.urls import include, re_path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from graphene_django.views import GraphQLView
from regulations_example.api.schema import schema


urlpatterns = [
    re_path(r"^admin/", include(wagtailadmin_urls)),
    re_path(r"^graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    re_path(r"", include(wagtail_urls)),
]
