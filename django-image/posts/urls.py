from django.urls import path

from .views import (
    HomePageView, CreatePostView, UpdatePostView, DeletePostView
)

# our webapps routing table. 
# '' specifies what to serve when nothing is entered in the url other than http://host:port
# 'post/' specifies what to serve when http://host:port/post is entered
# - this implicitly expects a post.html to exist in the app/templates/app folder
# the name is like a tag that our app can refer to when redirecting urls
# '<int:id>/update' specifies where to go to update the page
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/', CreatePostView.as_view(), name='upload'),
    path('<int:id>/update/', UpdatePostView.as_view(), name='update'),
    path('<int:id>/delete/', DeletePostView.as_view(), name='delete'),
]
