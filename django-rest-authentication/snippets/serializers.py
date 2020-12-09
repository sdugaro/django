from rest_framework import serializers

from django.contrib.auth.models import User

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# Analagous to Djangos ModelForm/Form Meta class code simplification
# REST has a ModelSerializer/Serializer simplification idiom
# Snippets are associated with the user that created them in the
# SnippetList view. Add an owner field here to recieve it.
class SnippetSerializer(serializers.ModelSerializer):

    # the source argument controls which attribute is used to populate a field
    # it can point at any attribute on the serialized instance
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'owner', 'title', 'code', 'linenos', 'language', 'style']


# We need a serializer to transmit user data coupled with
# some user information, such as username and authenticaion_id

class UserSerializer(serializers.ModelSerializer):

    snippets = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

