from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('',
         TemplateView.as_view(template_name="home.html"), name='home'),
    path('report/retail',
         TemplateView.as_view(template_name="retail.html"), name='retail'),
    path('report/marketing',
         TemplateView.as_view(template_name="marketing.html"), name='marketing'),
]

