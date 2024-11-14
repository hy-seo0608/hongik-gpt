from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'user_question',
            'model_classification',
            'model_answer',
            'user_intended_classification',
            'user_desired_answer',
        ]
        widgets = {
            'user_question': forms.Textarea(attrs={'readonly': 'readonly'}),
            'model_classification': forms.TextInput(attrs={'readonly': 'readonly'}),
            'model_answer': forms.Textarea(attrs={'readonly': 'readonly'}),
        }

