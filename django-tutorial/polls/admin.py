from django.contrib import admin

from .models import Question, Choice


#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):

    # reorder fields for a Qeustion redcord
    #fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date']}),
        ('Optional Information', {'fields': ['question_pdf', 'question_img']})
    ]
    # Choice objects are editon on the QuetionAdmin page
    inlines = [ChoiceInline]

    # display individual fields and method results on admin table view
    list_display = ('question_text', 'pub_date', 'was_published_recently',
                    'question_pdf', 'question_img')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.AdminSite.site_header = "Polls Administration"
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)


