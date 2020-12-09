from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

# route host:port/<appname> to an appropriate module
# that module is likely to have its own routing table.
urlpatterns = [
    path('polls/', include('polls.urls')),
    #path('polls/', include('polls.urls'), namespace='polls'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='landing.html'), name='root')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
