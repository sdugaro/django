from django.contrib import admin
from .models import Snippet

# use Native Djangos admin page to create and manage
# (administer) Model Instances.
admin.site.register(Snippet)
