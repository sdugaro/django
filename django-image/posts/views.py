from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy  

from .models import Post
from .forms import PostForm

# https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/
# ListView.object_list will contain the list of objects that the view operates on
# this field can be can be used in the iteration markup of a template.html
# {% for post in object_list %} wich provides an instance of a model object

# Create your views here.
# A View needs a Model class to describe the data to get from the db and a 
# template_name that specifies the file to search for in the project path to 
# insert the database data into via markup such that the page can be rendered.
# 
# project wide templates are maintained at the $BASEDIR/templates
# app level templates are maintained at $BASEDIR/app/templates/app/
# by default, if template_name is not specified, django constructs a default
# template file name from the app name, the model name, and the view type:
# ie for our app `posts` model `Post` and List view type -> posts/post_list.html
# specifying a template_name will take precedence over the default 

class HomePageView(ListView):
    model = Post
    template_name = 'posts/home.html'  
    #template_name = 'posts/post_list.html'  

# allow site users to upload an image as they wont have access to the
# admin page, privy to a supersuer with login credentials
# https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView
# https://docs.djangoproject.com/en/3.1/ref/urlresolvers/#reverse-lazy
# Subclass Djangos CreateView, providing a Model, ModelView and template.html
# page to render, along with a page to redirect to when the submission is complete
# as we dont want to just leave the page there with no feedback that data has
# been entered into the db, leading to multiple clicks and multiple db entries.

class CreatePostView(CreateView): # new
    model = Post
    form_class = PostForm
    template_name = 'posts/post.html'
    #template_name = "posts/post_create.html"
    success_url = reverse_lazy('home') # the routing url name in urls.py


# allow site users to update the data for a specific record in the db
class UpdatePostView(UpdateView):
    form_class = PostForm
    #template_name = 'posts/update.html'
    template_name = "posts/post_update.html"
    success_url = reverse_lazy('home') # the routing url name in urls.py

    # primary job is to update a specific record
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)

    def form_valid(self, form):
        # see what data is coming through here
        print(form.cleaned_data)
        return super().form_valid(form)


# Allow site users to delete a specific record in the db.
# We are intentionally avoiding a template to redirect to when a GET is issued
# which normally provides data to a post_confirm_delete.html template. Instead
# we confirm the delete via onclick in the corresponding anchor of record in
# the ListView of the home page and just go ahead an delete the record. We do
# this by overriding the get() method such that we POST the database deletion
# of the particular object as soon as the GET is issued by the anchor.

class DeletePostView(DeleteView):
    form_class = PostForm

    # built into class based views
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)

    def get(self, request, *args, **kwargs):
        print("--> GET: posting delete without confirm_delete.html template", request)
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('home')


