from django import forms
from ask.models import Question, Comment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = {
            'question',
            'picture',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            'content'
        }
