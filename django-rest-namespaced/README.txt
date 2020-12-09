#---------------------------------------------------------------------------
# To Generate Documentation we need to generate a schema from our webapp
#
# This is straightforward as a plugin will provide the documentation
# but it does requrie some basic system config
#
# 1. pip install django-extenstions  # to install the rest schema generator
# 2. pip install uritemplate         # used by the rest schema generator
# 3. ./manage.py generateschema      # to stdout some json schema
# 4. copy it to a static directory
# 5. point to it with an openapi doc generator template that loads static
# 6. route a generic Django TemplateView to serve it up.
# 7. ./manage.py runserver and visit http://127.0.0.1:8000/snippets/redoc/

/home/sdugaro/SRC/django-rest-doc
]> pip install django-extensions

/home/sdugaro/SRC/django-rest-doc
]> pip install uritemplate

/home/sdugaro/SRC/django-rest-doc
]> ./manage.py help
[rest_framework]
   generateschema

/home/sdugaro/SRC/django-rest-doc
]> ./manage.py help generateschema
usage: manage.py generateschema [-h] [--title TITLE] ...
Generates configured API schema for project.

optional arguments: ...
  --format {openapi,openapi-json}
...

/home/sdugaro/SRC/django-rest-doc
]> ./manage.py generateschema --format openapi-json > openapi-schema.json

]> mkdir static/schema
]> mkdir templates/doc
]> cp openapi-schema.json static/schema

]> vi templates/doc/redoc.html

{%load static %}
<!DOCTYPE html>
<html>
  <head>
    <title>ReDoc</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <!-- ReDoc doesn't change outer page styles -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
      <redoc spec-url="{% static '/schema/openapi-schema.json' %}"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
  </body>
</html>

/home/sdugaro/SRC/django-rest-doc
]> vi config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('snippets.urls')),

    # route a generic Django TemplateView to serve the reDoc template.
    # `extra-context` get the view name of teh SchemaView
    path('redoc/', TemplateView.as_view(
        template_name='docs/redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
]

#---------------------------------------------------------------------------

# needed to in config/settings.py to override rest_framework
# css and js scripts from within our own project folders

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# STATIC_ROOT:
#   the folder where static files will be stored after using
#   ./manage.py collectstatic (copy to directory)
#   this does nothing for development, only required for deployment
# STATICFILES_DIRS:
#   the list of folders where Django will search for additional
#   static files
# STATIC_URL:
#   the url, relative to which, static files will be served
#

STATIC_URL = '/static/'
#STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / "static"]  # for loc


# When overriding templates from another project such as the
# rest_framework api.html tempate, Djangos template loader
# will search DIRS before APP_DIRS in order to pick it up
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # app override of reset_framework/templates
        'DIRS': [BASE_DIR / 'templates'],
        #'DIRS': [],
        'APP_DIRS': True, # search app level templates (no worky?)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

