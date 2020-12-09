from django.urls import path, include
from snippets import views

from rest_framework.routers import DefaultRouter
#from rest_framework.urlpatterns import format_suffix_patterns

# Use a conventional Router from the rest_framework
# instead of designing your own URL configuration.
# Create a DefaultRouter and register viewsets

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# Include conventional urls derived from Router ViewSets
# Note that the DefaultRouter also determines the api_root
# function based view automatically the view class
urlpatterns = [
    #path('', views.api_root),
    path('', include(router.urls))
]

# allow for suffixed endpoint redirection
#urlpatterns = format_suffix_patterns(urlpatterns)


