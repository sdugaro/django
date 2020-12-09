from rest_framework import serializers

from django.contrib.auth.models import User

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# Snippets are associated with the user that created them in the
# SnippetList view. Add an owner field here to recieve it.
# Subclass a HyperlinkedModelSerializer rather than a ModelSerializer
# to create a hyperlinked style between entities
class SnippetSerializer(serializers.HyperlinkedModelSerializer):

    # the source argument controls which attribute is used to populate a field
    # it can point at any attribute on the serialized instance
    owner = serializers.ReadOnlyField(source='owner.username')

    # ensure any format suffixed hyperlinks this field returns
    # should use the html format suffix
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['id', 'owner', 'title', 'code',
                  'linenos', 'language', 'style', 'highlight']


# We need a serializer to transmit user data coupled with
# some user information, such as username and authenticaion_id
# Subclass a HyperlinkedModelSerializer rather than a ModelSerializer
# to create a hyperlinked style between entities
class UserSerializer(serializers.HyperlinkedModelSerializer):

    snippets = serializers.HyperlinkedRelatedField(many=True,
                                                   view_name='snippet-detail',
                                                   read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets', 'url']

