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
import pandas as pd
from utils.intent import predict
from utils.FindAnswer import FindAnswer
from .forms import FeedbackForm
from .models import Feedback


# 챗봇 응답 처리 뷰
@login_required(login_url="common/login")
def index(request):
    return render(request, "dialog/index.html")


# 피드백 저장 뷰
@login_required
def feedback_save(request):
    """
    Save feedback data received from the user
    """
    if request.method == "POST":
        data = json.loads(request.body)

        # 피드백 데이터 수집
        feedback_text = data.get("user_desired_answer", "")  # 사용자가 입력한 피드백
        user_question = data.get("user_question", "")  # 사용자 질문
        response_id = data.get("responseId")  # 응답 ID

        # 사용자 질문을 사용하여 예측 클래스와 답변 가져오기
        best_sim_idx, predicted_sentence = predict(user_question)  # 모델이 예측한 클래스 ID와 질문
        model_answer, buttons, mode = FindAnswer(best_sim_idx)  # 예측 클래스에 대한 답변, 버튼, 모드

        # 새로운 Feedback 객체를 저장
        Feedback.objects.create(
            user_id=request.user.id,
            user_question=user_question,
            user_desired_answer=feedback_text,
            model_classification=predicted_sentence,
            model_answer=model_answer,
        )

        return JsonResponse({"message": "피드백을 주셔서 감사합니다!"})
    else:
        return JsonResponse({"message": "잘못된 요청입니다."}, status=400)
