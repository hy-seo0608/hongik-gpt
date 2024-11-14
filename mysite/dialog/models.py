from django.db import models
from django.contrib.auth.models import User

import datetime
from django.utils import timezone


# 사용자 피드백을 받기 위한 db 테이블
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_question = models.TextField()                          # 사용자가 한 질문
    model_classification = models.CharField(max_length=255)     # 대분류, 질문 클래스
    model_answer = models.TextField()                           # 모델이 출력한 답변
    user_intended_classification = models.CharField(max_length=255, blank=True, null=True) # 사용자가 원한 질문 분류 (대분류, 질문 클래스)
    user_desired_answer = models.TextField(blank=True, null=True)   # 사용자가 원한 답변 (사용자가 입력)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} on {self.created_at}"