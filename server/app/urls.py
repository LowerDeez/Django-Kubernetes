from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path

from apps.core.views import image_upload

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    # url(r'', include('apps.frontend.urls')),
    path("", image_upload, name="upload"),
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [url(r"^rosetta/", include("rosetta.urls"))]

if settings.DEBUG:
    urlpatterns += [url(r"^", include("markup.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r"^__debug__/", include(debug_toolbar.urls)),
        ]
