from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogIndexView.as_view(), name='blog_index'),
    path('<int:pk>/', views.BlogView.as_view(), name='blog_detail'),
    path('results/', views.SearchView.as_view(), name='blog_search'),
    path('<category>/', views.BlogCategoryView.as_view(), name='blog_category'),
]
