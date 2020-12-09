from django.urls import path
from snippets import views

# support file extensions on endpoints

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]

# totally optional, but provides a simple clean way of
# referring to a specific format
urlpatterns = format_suffix_patterns(urlpatterns)


