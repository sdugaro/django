from django.shortcuts import render
from django.views import generic, View
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q

from .models import Post, Category, Comment
from .forms import CommentForm

# Create your views here.


class BlogIndexView(generic.ListView):
    template_name = 'blog/blog_index.html'

    def get_queryset(self):
        """Return all Posts ordered by creation date """

        result = Post.objects.all()
        result = result.order_by('-created_on')
        print(f"{result}")
        return result


class BlogCategoryView(generic.ListView):
    template_name = 'blog/blog_category.html'

    def get_context_data(self, **kwargs):
        """ pass the category slug to the template """
        print(f"{self.kwargs}")
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def get(self, request, *args, **kwargs):
        """Return all Posts filtered by category """
        user = self.request.user
        category = kwargs.get('category')

        # categories is the ManyToMany Post field object name
        result = Post.objects.filter(categories__name__contains=category)
        result = result.order_by('-created_on')
        print(f"{result}")
        self.queryset = result

        return super().get(request, *args, **kwargs)


class BlogDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        print(f"get_context_data {kwargs}")
        print(f"get_context_data {self.kwargs}")
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        comments = Comment.objects.filter(post=post)
        context['form'] = CommentForm()
        context['comments'] = comments
        context['post'] = post
        return context


class BlogFormView(SingleObjectMixin, generic.FormView):
    model = Post  # for SingleObjectMixin
    template_name = 'blog/blog_detail.html'
    form_class = CommentForm  # for FormView

    def form_valid(self, form):
        print(f"form_valid {self.kwargs}")

        if not self.request.user.is_authenticated:
            return HttpResponseForbidden()

        # we can get an object instance via the URL with get_object()
        # which is why we need to inherit from SingleObjectMixin and
        # populate the model attribute with the queryset class
        self.object = self.get_object()
        comment = Comment(
            author=form.cleaned_data["author"],
            body=form.cleaned_data["body"],
            post=self.object
        )
        comment.save()  # by django.db.models.Model inheritance

        return super().form_valid(form)

    def get_success_url(self):
        print(f"get_success_url {self.kwargs}")
        return reverse('blog_detail', kwargs={'pk': self.object.pk})


class BlogView(View):

    def get(self, request, *args, **kwargs):
        view = BlogDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BlogFormView.as_view()
        return view(request, *args, **kwargs)


class SearchView(generic.ListView):
    model = Post
    template_name = 'blog/blog_search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        #result = Post.objects.filter(title__contains=query)
        result = Post.objects.filter(
            Q(title__contains=query) | Q(body__contains=query)
        )
        result = result.order_by('-created_on')
        return result


