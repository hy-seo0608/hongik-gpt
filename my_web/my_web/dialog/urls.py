from django.urls import path

from . import views

app_name = "dialog/"
urlpatterns = [
    path('', views.ChatbotView.as_view(), name="index"),
]