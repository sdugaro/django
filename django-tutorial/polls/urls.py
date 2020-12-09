from django.urls import path, re_path, register_converter, include
from django.contrib.auth import views as auth_views

from . import views
from . import converters

# Register any Custom Path Converters for use in urlpatterns
#register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoToFourDigitYearConverter, 'yyyy')

# Specify the app namespace for reverse resolution of urls
app_name = 'polls'

# for a specific app, route host:port/appname/<pattern>
# to the appropriate handlers in the apps view module
urlpatterns_examples = [

    #path('', views.index, name='index'),
    path('2011/', views.index),
    #path('<int:year>/', views.index),   # anything int() can cast
    path('<int:year>/<int:month>/', views.index),
    path('<int:year>/<int:month>/<slug:slug>/', views.index),
    path('<int:year>/<int:month>/<slug:slug>/<uuid:user>', views.index),
    path('<int:year>/<int:month>/<slug:slug>/<uuid:user_id>/<path:path>', views.index),
    re_path(r'^toc/$', views.index),
    re_path(r'^bio/(?P<username>\w+)/$', views.index),
    path('<yyyy:yyyy>/', views.index),    # to kwargs
    #re_path(r'([0-9]+)/', views.index),  # to args

    # http://127.0.0.1:8000/polls/index/2020/hello/__Init0-9__/rest/of/it/?name=steve&age=25&age=45
    # django.http.HttpRequest(<WSGIRequest:
    #  GET '/polls/index/2020/hello/__Init0-9__/path/?name=steve&age=45'>,
    #  args: ()
    #  kwargs: {'int_key':2020, 'str_key':'hello', 'slug_key':'__Init0-9__', 'path_key':'path/'})
    #  request.GET: <QueryDict: {'name': ['steve'], 'age': ['45']}>
    # djgango.http.HttpResponse()
    # [25/Nov/2020 05:35:46]
    #  "GET /polls/index/2020/hello/__Init0-9__/path/?name=steve&age=45 HTTP/1.1" 200 40
    #  responded to above HttpRequest with status code 200 (2xx are success codes 200=OK)
    path('index/<int:int_key>/<str:str_key>/<slug:slug_key>/<path:path_key>', views.index),
]


# Generic Class Based Views
# Use <pk> for the render instance argument by default
# as you do not need to call it with class based view
# since they do it for you, provided you adhere to the
# conventional setup.
urlpatterns = [

    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),  # requires id
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('pdf/', views.PdfListView.as_view(), name='pdf-list'),
    path('pdf/<int:pk>/', views.PdfDetailView.as_view(), name='pdf-detail'),
    path('pdf/<slug:slug>/', views.render_pdf_view,
         kwargs={'from': 'url_patterns'}, name='pdf-test'),


]

