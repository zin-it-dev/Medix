from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from oauth2_provider import urls as oauth2_urls
from debug_toolbar.toolbar import debug_toolbar_urls

from core.settings import base

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^o/', include(oauth2_urls, namespace='oauth2_provider')),
    re_path(r'^', include('apis.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if base.DEBUG:
    urlpatterns += debug_toolbar_urls()