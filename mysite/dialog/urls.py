from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "dialog"
urlpatterns = [
    path("", views.index, name="index"),
    path("answer/<int:question_id>/", views.get_answer, name="get_answer"),     # 챗봇 응답을 위한 URL
    path("feedback/", views.feedback_save, name="feedback_save"),               # 피드백 폼 제출 URL
]
