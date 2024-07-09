from django.db import models

import datetime
from django.utils import timezone
"""
모델의 활성화를 위해서는 
1. 데이터베이스 스키마 생성
2. 객체에 접근하기 위한 Python 데이터베이스 접근 API를 생성
"""

# Create your models here.
class Question(models.Model) :
    question_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.question_text
    
    def was_published_recently(self) :
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model) :
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    votes = models.IntegerField(default=0)

    def __str__(self) :
        return self.choice_text
    
    

class Answer(models.Model) :
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.answer_text
