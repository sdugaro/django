from django.shortcuts import render
from django.views import generic, View
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy

from .models import Entry, Author
from .forms import EntryForm

import base64

# Create your views here.


class HomeView(generic.ListView):
    template_name = 'blog/home.html'

    def get_queryset(self):
        """Return all Posts ordered by creation date """

        result = Entry.objects.all()
        result = result.order_by('-pub_date')
        print(f"{result}")
        return result


class EntryView(generic.DetailView):
    model = Entry
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        print(f"get_context_data {kwargs}")
        print(f"get_context_data {self.kwargs}")
        context = super().get_context_data(**kwargs)
        detail = Entry.objects.get(pk=self.kwargs['pk'])
        raw_image = detail.featured_image.read()
        image = base64.b64encode(raw_image).decode('ascii')
        context['entry'] = detail
        context['image'] = image
        print(f"{context}")
        return context


class AuthorView(generic.DetailView):
    model = Author
    template_name = 'blog/author_detail.html'

    def get_context_data(self, **kwargs):
        """ get the binary image from the database and
        add it to the context for streaming directly into
        the browser
        """
        print(f"get_context_data {kwargs}")
        print(f"get_context_data {self.kwargs}")
        context = super().get_context_data(**kwargs)
        detail = kwargs['object']
        image = base64.b64encode(detail.avatar.read()).decode('ascii')
        context['author'] = detail
        context['image'] = image
        print(f"{context}")
        return context

    def get_object(self, queryset=None):
        """Return the Author for the specific slug """
        print(f"get_object {self.kwargs}")
        slug = self.kwargs['name']
        author = Author.objects.get(name=slug)
        return author


class CreateEntryView(generic.CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'blog/create.html'
    # designate which fields we want on the creation page
    # fields = '__all__'
    #fields = ['headline', 'body_text', 'authors', 'rating', 'featured_image']


class UpdateEntryView(generic.UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'blog/update.html'


class DeleteEntryView(generic.DeleteView):
    model = Entry
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('home')


