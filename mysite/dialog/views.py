from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import FormView, TemplateView
from django.template import loader
from django import forms
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import socket, json
from .models import Question, Answer

# Create your views here.


@login_required(login_url="common/login")
def index(request):
    return render(request, "dialog/index.html")
