from django.urls import path
from snippets import views

# support file extensions on endpoints
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

# allow for suffixed endpoint redirection
urlpatterns = format_suffix_patterns(urlpatterns)


