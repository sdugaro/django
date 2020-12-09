# HttpRespone must be instantiated, populated, and returned by a view
# Likewise, if we want to return some JSON instead of HTML
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# We will need a JSONParser to deserialize JSON data into the view
from rest_framework.parsers import JSONParser

# We make use of our model and serializer classes to do this
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# The root of the API will be a view that supports listing all
# existing model records, and creating a new Snippet model.
# We can make this view csrf_exempt because we want clients
# that do not have a csrf token to be able to POST

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':      # list
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':   # create
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# We also need a view that corresponds to an individual Model instance.
# We can use this to retrieve, update, or delete the Model instance.

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':       # retrieve
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':     # update
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':  # delete
        snippet.delete()
        return HttpResponse(status=204)
