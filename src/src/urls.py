from django.conf.urls import url, handler400, handler403, handler404, handler500
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_URL)


handler400 = 'app.views.error_400'
handler403 = 'app.views.error_403'
handler404 = 'app.views.error_404'
handler500 = 'app.views.error_500'
