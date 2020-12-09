from rest_framework import generics

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# Root View to List and Create

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

# Instance View to Detail, Update, Delete

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
