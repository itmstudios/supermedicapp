from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_title = "Администрирование сайта"
admin.site.site_header = "Супер медик"
admin.site.index_title = "Добро пожаловать в админ панель"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("supermedicapp.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
