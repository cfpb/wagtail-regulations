from django.conf.urls import include, url

import wagtail

if wagtail.VERSION >= (2, 0):  # pragma: no cover
    from wagtail.admin import urls as wagtailadmin_urls
    from wagtail.core import urls as wagtail_urls
else:  # pragma: no cover
    from wagtail.wagtailadmin import urls as wagtailadmin_urls
    from wagtail.wagtailcore import urls as wagtail_urls


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r"", include(wagtail_urls)),
]
