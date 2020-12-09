from rest_framework import generics
from rest_framework import permissions

from rest_framework.response import Response

from django.contrib.auth.models import User

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


# Database Views to List and Create
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # ensure authenticated requests get read-write access
    # while unauthenticated requests get read-only access
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # hook to associate the user who created the snippet with
    # the snippet instance. ie. pass the serializer.create()
    # an additional owner field with validated data from
    # the request
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Database Instance Views to Detail, Update, Delete
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # ensure authenticated requests get read-write access
    # while unauthenticated requests get read-only access
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


# For authentication
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

