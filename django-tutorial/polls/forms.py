from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField


class SignUpForm(UserCreationForm):

    email = EmailField(label="User Email", max_length=87,
                       help_text="Required and validated.")

    class Meta:
        model = User
        fields = ("username", "email")

