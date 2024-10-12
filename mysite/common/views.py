from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib import auth
from .forms import UserForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.db.utils import IntegrityError


def logout_view(request):
    logout(request)
    return redirect("common:login")


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"], email=request.POST["email"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string(
                "user_activate_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                    "token": account_activation_token.make_token(user),
                },
            )
            mail_subject = "[Hongpt] 회원가입 인증 메일입니다."
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                "입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>"
                "</div>"
            )
    else:
        form = UserForm()
    return render(request, "common/signup.html", {"form": form})


def activate(request, uid64, token):

    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("/")
    else:
        return HttpResponse("비정상적인 접근입니다.")


def page_not_found(request, exception):
    return render(request, "common/404.html", {})
