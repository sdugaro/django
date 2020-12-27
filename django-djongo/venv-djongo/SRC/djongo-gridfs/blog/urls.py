from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.EntryView.as_view(), name='detail'),
    path('author/<slug:name>/', views.AuthorView.as_view(), name='author'),
    path('create/', views.CreateEntryView.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdateEntryView.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteEntryView.as_view(), name='delete'),
]

