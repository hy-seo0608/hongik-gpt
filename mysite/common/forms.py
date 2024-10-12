from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")

        if email and not email.endswith("@naver.com"):
            self.add_error("email", ValidationError("이메일은 @naver.com 도메인만 사용할 수 있습니다."))

        return cleaned_data
