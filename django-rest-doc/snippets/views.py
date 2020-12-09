from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.metadata import BaseMetadata
from rest_framework import renderers

from django.contrib.auth.models import User

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


# Root View
class APIRoot(APIView):
    """
    This is the landing page for the Snippet API.
    It allows you to create and save snippets of code that
    will have syntax highlighting applied by `pygments`
    """

    def get(self, request, format=None):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'snippets': reverse('snippet-list', request=request, format=format)
        })


# Create, List, Detail, Delete Snippet Views
# Custom Highlight View for a particular Snippet's final HTML
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides the following actions
    `list` `create` `retrieve` `update` and `destroy`
    We additionally provide an extra `highlight` action
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

