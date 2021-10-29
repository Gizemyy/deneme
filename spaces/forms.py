from django import forms
from spaces.models import Spaces
from ask.models import SpaceQuestion,SpaceQuestionComment
class SpaceForm(forms.ModelForm):
    class Meta:
        model = Spaces
        fields = {
            'title',
            'description',
            'profile_pic',
        }

class SpaceQuestionForm(forms.ModelForm):
    class Meta:
        model = SpaceQuestion
        fields = {
            'question',
            'picture',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = SpaceQuestionComment
        fields = {
            'content'
        }
