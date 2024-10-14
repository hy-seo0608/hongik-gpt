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

        if email and not (email.endswith("@hongik.ac.kr") or email.endswith("@g.hongik.ac.kr")):
            self.add_error("email", ValidationError("학교 이메일 (@hongik.ac.kr 또는 @g.hongik.ac.kr)을 입력해주세요"))

        return cleaned_data
