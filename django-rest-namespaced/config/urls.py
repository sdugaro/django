"""
config URL Configuration

The `urlpatterns` list routes URLs to views.
https://docs.djangoproject.com/en/3.1/topics/http/urls/

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('snippets.urls')),

    # route a generic Django TemplateView to serve the reDoc template.
    path('redoc/', TemplateView.as_view(
        template_name='docs/redoc.html',
    ), name='redoc'),

    # use djangos {% url name %} directive to point to this TemplateView.
    # we dont need to change the url in the doc template that way, we can
    # do it from here instead, simply referencing schema_url value
    path('redoc_r/', TemplateView.as_view(
        template_name='docs/redoc.html',
        extra_context={'schema_url': '/static/schema/openapi-schema.json'}
    ), name='redoc_r'),

    # route a generic Django TemplateView to serve the Swagger-UI template.
    path('swagger/', TemplateView.as_view(
        template_name='docs/swagger.html',
    ), name='swagger'),

    # use "{% url 'swagger_r' %}" where a schema url is required for config
    path('swagger_r/', TemplateView.as_view(
        template_name='docs/swagger_r.html',
        extra_context={'schema_url': '/static/schema/openapi-schema.json'}
    ), name='swagger_r'),
]

