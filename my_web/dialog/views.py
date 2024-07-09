from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import FormView, TemplateView
from django.template import loader
from django import forms

from .models import Choice, Question, Answer

# Create your views here.

class ChatbotView(TemplateView):
    template_name = 'dialog/index.html'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['question_text'] = Question.objects.all()
        return context
    
    def post(self, request, *arg, **kwargs) :
        question = request.POST.get('question')
        user_question = Question.objects.create(question_text=question)
        bot_response = get_answer(question)
        bot_message = Answer.objects.create(answer_text=bot_response, question=user_question)
        return JsonResponse({'answer' : bot_response})
        

def get_answer(question):
    # 여기에서 실제 챗봇 로직을 구현합니다.

    # 의도분류

    label = 2

    return "This is a fixed answer to the question: " + question

# class IndexView(generic.ListView) :
#     template_name = "dialog/index.html"
#     context_object_name = "latest_question_list"

#     def get_queryset(self) :
#         return Question.objects.order_by("-pub_date")[:5]

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = "dialog/detail.html"


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = "dialog/results.html"

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))