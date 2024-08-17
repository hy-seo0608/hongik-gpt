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

import socket, json
from .models import Question, Answer

# Create your views here.

host = "127.0.0.1"
port = 5050


class ChatbotView(LoginRequiredMixin, TemplateView):
    template_name = "dialog/index.html"
    login_url = "common:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_txt"] = Question.objects.all()
        return context

    @staticmethod
    def send_question_to_server(question):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        json_data = {
            "question_txt": question,
        }
        message = json.dumps(json_data)
        client_socket.send(message.encode())
        answer = client_socket.recv(2048).decode()

        client_socket.close()
        ret_data = json.loads(answer)
        return ret_data

    def post(self, request, *arg, **kwargs):
        question = request.POST.get("question")
        user_question = Question.objects.create(question_text=question)
        bot_response = self.send_question_to_server(question)
        # bot_message = Answer.objects.create(answer_text=bot_response, question=user_question)
        return JsonResponse({"answer": bot_response["Answer"]})
