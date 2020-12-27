from django import forms
from .models import Entry


class EntryForm (forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['blog', 'headline', 'body_text', 'authors', 'rating', 'featured_image']

        # connect bootstrap form styling

        widgets = {
            'blog': forms.Select(attrs={'class': 'form-control'}),
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body_text': forms.Textarea(attrs={'class': 'form-control'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'})
        }


