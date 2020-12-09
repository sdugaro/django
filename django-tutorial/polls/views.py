from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.conf import settings

from django.http import FileResponse, Http404
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Question, Choice
from .logger import POLLS_BOTH as logger
from .signals import pdf_done
from .forms import SignUpForm
from .apps import PollsConfig
from .utils import __breakpoint__

#
# Custom Paginator for Long Paginations
# ---------------------------------------

class BootstrapPaginator(Paginator):
    """
    A paginator that does not return the entire range, rather
    a few wing pages on either side of the current page.
    """
    def __init__(self, *args, **kwargs):
        """Initialize Paginator parameters, defaulting extended parameters

        Args:
            wing_pages (int): default 2
                the number of pages shown before and after the current page.
            max_pages (int): defaut 5
                the total number of pages to show in the pagination range
        """
        self.max_pages = kwargs.pop('max_pages', 5)
        self.wing_pages = kwargs.pop('wing_pages', 2)
        #super(BootstrapPaginator, self).__init__(*args, **kwargs)  # Py2k
        super().__init__(*args, **kwargs)  # Py3k

    def _get_page(self, *args, **kwargs):
        self.page = super(BootstrapPaginator, self)._get_page(*args, **kwargs)
        return self.page

    @property
    def page_range(self):
        fold_min = max(self.page.number - self.wing_pages, 1)
        fold_max = fold_min + self.max_pages
        logger.debug(f"fold_min[{fold_min}] fold_max[{fold_max}]")
        if fold_max > self.num_pages:
            fold_min = self.num_pages - self.max_pages + 1
            fold_max = self.num_pages + 1

        fold_range = range(fold_min, fold_max)
        logger.debug(f"fold_range={fold_range}")
        return fold_range


# Generic Class Based Views
# ---------------------------
class HomeView(generic.ListView):
    #template_name = 'polls/home.html'
    template_name = 'polls/home_bootstrap.html'
    context_object_name = 'latest_question_list'
    paginate_by = 1
    paginator_class = BootstrapPaginator

    def get_queryset(self):
        """Return the last five published questions.
        Do not including those set to be published in the future:
        """
        #return Question.objects.order_by('-pub_date')[:5]

        # filter timezones less than now
        result = Question.objects.filter(pub_date__lte=timezone.now())
        #result = result.order_by('-pub_date')[:5]
        result = result.order_by('-pub_date')

        objects = '\n'.join([str(x) for x in result])
        #logger.debug("\n{}".format('\n'.join([str(x) for x in result])))
        logger.info(f"Ordered [{result.count()}] Questions by reverse pub_date")
        logger.debug(f"\n{objects}")
        logger.done("get_queryset()")
        logger.error("Test")
        logger.critical("Boom!")

        return result


class DetailView(generic.DetailView):
    model = Question
    #template_name = 'polls/detail.html'
    template_name = 'polls/detail_bootstrap.html'

    def get_context_data(self, **kwargs):
        # get context from base implementation
        context = super().get_context_data(**kwargs)
        context['extra'] = "data"
        return context


class ResultsView(generic.DetailView):
    model = Question
    #template_name = 'polls/results.html'
    template_name = 'polls/results_bootstrap.html'

    def get_object(self):
        # run logic before base class calls get_object
        __breakpoint__(False)
        #import pdb; pdb.set_trace()
        print("About to get_object results")
        obj = super().get_object()
        print(f"got {obj}")
        return obj


class SignUpView(SuccessMessageMixin, generic.CreateView):
    #form_class = UserCreationForm
    form_class = SignUpForm
    success_url = reverse_lazy('polls:login')
    template_name = 'registration/signup.html'
    #success_message = "Account successfully created!"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('polls:home')
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(type(response))
        logger.debug("--> New user registered. Now send email.")
        logger.debug(self.request)

        # at this point, the User should be saved in the DB,
        # but rather than query the DB, we can get what we need
        # from the form just as the DB did
        user = form.cleaned_data['username']
        email = form.cleaned_data['email']

        context = {
            'appurl': response.url,
            'appname': PollsConfig.name,
            'appmail': PollsConfig.email,
            'siteurl': settings.SITE_URL,
            'sitemail': settings.DEFAULT_FROM_EMAIL,
            'sitename': settings.SITE_NAME,
            'username': user,
        }
        subject = f"Welcome to {context['appname']}"
        body = render_to_string("registration/welcome_email.html", context)
        email = EmailMessage(subject, body, context['sitemail'], [email])
        email.content_subtype = "html"
        try:
            email.send()
            message = "Account created! Check your email for more info."
            messages.success(self.request, message)
        except Exception as e:
            logger.warning(e)
            message = "Account created, but email failed."
            messages.warning(self.request, message)
        return response


class PdfListView(generic.ListView):
    model = Question
    template_name = 'polls/pdf_list.html'


class PdfDetailView(generic.DetailView):
    model = Question
    template_name = 'polls/pdf_detail.html'
    context_object_name = 'question'  # same by default (from Question)

    def get_context_data(self, **kwargs):
        # need to recieve pk for the specific object instance to be handled
        # in the specified template. We can add local context vars here.
        # This is where we parse and process any query string modifiers
        user = self.request.user
        query_dict = dict(self.request.GET)
        logger.debug(f"-> PdfDetailView|get_context_data]\nuser: {user}")
        logger.debug(f"-> PdfDetailView|get_context_data]\nself.request.GET: {query_dict}")
        logger.debug(f"-> PdfDetailView|get_context_data]\nself.kwargs: {self.kwargs}")
        logger.debug(f"-> PdfDetailView|get_context_data]\nkwargs: {kwargs}")
        context = super().get_context_data(**kwargs)

        keys = query_dict.keys()
        context['format'] = 'pdf'
        context['download'] = False
        context['engine'] = 'xhtml2pdf'
        context['user'] = user

        if 'html' in keys:
            context['format'] = 'html'
        if 'download' in keys:
            context['download'] = True
        if 'reportlab' in keys:
            context['engine'] = 'reportlab'

        return context

    def pdf_response_rl(self, question, filename, download=False):
        """
        Use the ReportLab api and the Model Objects provided by the context
        dict in this views pipeline.
        """
        import reportlab.platypus as RL
        import reportlab.lib.styles as SL
        from io import BytesIO

        flo = []
        out = BytesIO()  # create a byte buffer to hold PDF data
        pdf = RL.SimpleDocTemplate(out)
        pdf.showBoundary = 1
        pdf.leftMargin = pdf.rightMargin = pdf.leftMargin / 2
        pdf.topMargin = pdf.bottomMargin = pdf.topMargin / 2

        ss = SL.getSampleStyleSheet()
        h1 = RL.Paragraph("Question:", ss['Heading1'])
        h2 = RL.Paragraph(f"{str(question)}", ss['Heading2'])
        h3 = RL.Paragraph("Choices:", ss['Heading3'])
        hl = RL.HRFlowable(width='100%')

        if question.question_img:
            img = RL.Image(question.question_img.path, width=100, height=75, hAlign="LEFT")
            flo += [img, hl]

        flo += [h1, h2, hl, h3]

        ps = [RL.Paragraph(f"{str(c)} [{c.votes} votes]", ss['BodyText'])
              for c in question.choice_set.all()]
        ul = [RL.ListItem(x, value='sparkle') for x in ps]
        lf = RL.ListFlowable(ul, bulletType='bullet')
        flo += [lf]

        flo += [hl]
        try:
            pdf.build(flo)
        except Exception as e:
            message = (f"Unable to generate PDF from <hl><pre>{html}</pre>")
            return HttpResponse(message, status=500)

        out.seek(0)  # reset byte buffer pointer to the start

        if download:
            return FileResponse(out, as_attachment=True, filename=filename)
        return FileResponse(out, filename=filename)

    def pdf_response_xp(self, html, filename, download=False):
        """
        Use the xhtml2pdf to convert html to pdf an return
        it in an HttpResponse. Return an error message in the
        HttpResponse object if the conversion fails.
        """
        disposition = f'filename="{filename}"'
        if download:
            disposition = 'attachment;' + disposition

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = disposition

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            message = (f"Unable to generate PDF from <hl><pre>{html}</pre>")
            return HttpResponse(message, status=500)

        return response

    def render_to_response(self, context, **kwargs):
        # we expect polls/pdf/<pk>/?html or ?download.
        # ?html&download is not possible becuse every
        # HttpRequest has one corresponding HttpResponse
        logger.debug(f"-> PdfDetailView|render_to_response]\ncontext: {context}")
        logger.debug(f"-> PdfDetailView|render_to_response]\nkwargs: {kwargs}")
        #return HttpResponse(f"{context['format']}")

        engine = context['engine']
        username = context['user']
        question = context['question']
        download = context['download']
        filename = context.get('filename', 'report.pdf')

        template = get_template(self.template_name)
        html = template.render(context)

        if context['format'] == 'html':
            response = HttpResponse(html)
        elif engine == 'reportlab':
            response = self.pdf_response_rl(question, filename, download)
        else:
            response = self.pdf_response_xp(html, filename, download)

        # signal to log pdf generation
        pdf_done.send(self.__class__, user=username,
                      filename=filename, engine=engine)

        return response

#---------------------------------------------------------------------------
# Function Based Views
# - for illustration and test. Use Class Based Views.
#---------------------------------------------------------------------------


def vote(request, question_id):
    """
    Function based view requiring an id via url match or via
    context arguments in reverse redirect
    """
    # blocking without DB query
    #return HttpResponse("You're voting on question %s." % question_id)

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # message the error
        messages.error(request, "You didnt select a choice.")
        # Redisplay the question voting form.
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        messages.success(request, "Vote successfully registered!")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


""" Some callables for context dictionary values :

# Note that defining a static class method in python without a decorator
# does not allow you to call it from an instance of the class. Using a
# decorator is a more elegant and concise equivalent to:

class Calc:

    def add(x, y):
        return x + y

Calc.add = staticmethod(Calc.add)

>>> class Calc:
...   def add(*args):
...     return sum(map(float,args))
...
>>> Calc.add(1,2,3,'4','5','6')
21.0
>>> c = Calc()
>>> c.add(1,2,3,'4','5','6')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in add
TypeError: float() argument must be a string or a number, not 'Calc'

>>> class Calc:
...   @staticmethod
...   def add(*args):
...     return sum(map(float,args))
...
>>> c = Calc()
>>> Calc.add(1,2,3,'4','5','6')
21.0
>>>
"""


class Calculator:
    @staticmethod
    def add(*args):
        return sum(map(float, args))


def hello_world():
    return "Hello World"


def render_pdf_view(request, *args, **kwargs):
    """
    Render out a pdf file from an html template that displays what
    the user input as a query string in their browser request.

    path(
        'index/<int:int_key>/<str:str_key>/<slug:slug_key>/<path:path_key>',
        views.index)

    http://127.0.0.1:8000/polls/
        index/2020/hello/__Init0-9__/path/?name=steve&age=25&age=45

    Note that Django parses the query string into a <QueryDict> object
    and stores it in the HttpRequest.GET or HttpRequest.POST depending
    on whether the request was submitted via url or via a form button

    Note that the context passed to render is an empty dict by default.
    If a value in the dictionary is callable, the view will call it
    just before rendering the template.

    """
    url = request.get_full_path()
    query_dict = dict(request.GET)
    questions = Question.objects.all()
    print(f"--> render_pdf_view()\nargs:\n{args}\nkwargs\n{kwargs}")
    print(f"request.GET<QueryDict>:\n{query_dict}")
    print(f"questions<QuerySet>:\n{questions}")

    # Define the template
    template_name = 'polls/pdf_test.html'
    # Define the context we are passing to the template
    data = {
        'view_local_var': 'view_local_val',
        'view_local_var_1': Calculator.add(1, 2),
        'view_local_var_2': hello_world  # django will call this
    }
    data.setdefault('view_local_var3', Calculator.add(1, '2', 3))
    data['view_local_var4'] = Calculator.add('1.1', 2.2, '3.3', 4.4)
    data.update(query_dict)
    data.update(kwargs)

    context = {'data': data, 'url': url, 'db': questions}

    template = get_template(template_name)
    html = template.render(context)

    # Short-circuit template HTML render into an HttpResponse
    return render(request, template_name, context)

    # Create a Django response object, specifying content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # Display PDF in browser (default)
    response['Content-Disposition'] = 'filename="report.pdf"'
    # Download PDF as file
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Generate a PDF from the html template and write it into
    # the HttpResponse object to pass along to the browser.
    #pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    pisa_status = pisa.CreatePDF(html, dest=response)
    # If there was an error in PDF generation, return a page with an explanation
    # A 406 error code means server is unable to return acceptable content per
    # the clients request. A 500 means an unexpected condition on the server
    # side prevented the request from being fulfilled (code runtime errors)
    if pisa_status.err:
        message = (f"Unable to generate PDF from <hl><pre>{html}</pre>")
        return HttpResponse(message, status=500)
    return response


def index(request, *args, **kwargs):
    print(f"---> Routed to views.index({request},{args},{kwargs})")
    print(f"request.GET:{request.GET}")
    return HttpResponse("Hello, world. You're at the polls index.")


# /polls
# path('', views.home, name='home'),
# there are no matched arguments for the home view being
def home(request, *args, **kwargs):
    print("--->", args, kwargs)

    # blocking by returning text from python
    #questions = Question.objects.order_by('-pub_date')[:5]
    #output = ','.join([q.question_text for q in questions])
    #return HttpResponse(output)

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/home.html', context)


# /polls/5/
# path('<int:question_id>/', views.detail, name='detail'),
# urls.path(<int:question_id> describes the matched
# arguments that would be passed to the view
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


# /polls/5/results/
# path('<int:question_id>/results/', views.results, name='results'),
def results(request, question_id):
    # blocking without DB query
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})




