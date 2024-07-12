from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.user.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "f_name",
            "l_name",
            "user_image",
        )


class CustomUserChangeForm(UserChangeForm, forms.Form):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "f_name",
            "l_name",
            "addresses",
            "user_image",
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields["password"]
