from django import forms
from .models import Post

# A Model form is a class that lets you create a form page from a model
# https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#modelform

# We can configure the look of default modelform widgets via widgets=
# https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-field-types-or-widgets
# this doesnt look to work?

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'image', 'summary']
        widgets = {
            forms.Textarea(attrs={'rows':2, 'cols':150})
        }
