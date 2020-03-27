from django.conf import settings
from django.conf.urls import include, re_path
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from graphene_django.views import GraphQLView
from regulations_example.api.rest import api_router
from regulations_example.api.schema import schema


urlpatterns = [
    re_path(r"^django-admin/", admin.site.urls),
    re_path(r"^admin/", include(wagtailadmin_urls)),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    re_path(r"^api/v2/", api_router.urls),
    re_path(
        r"^graphql",
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)),
    ),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


urlpatterns = urlpatterns + [
    re_path(r"", include(wagtail_urls)),
]
