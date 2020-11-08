from django.contrib import admin

# Register your models here.
# after editing models, run makemigrations to generate new db schema for them
# then run migrate to update the database with these schemas

from .models import Post
admin.site.register(Post)
