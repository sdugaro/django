from django.contrib import admin

from .models import Blog, Entry, Author

# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    pass


class EntryAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Author, AuthorAdmin)



