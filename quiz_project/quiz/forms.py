from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Choice, CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
        labels = {
            'user_type': 'User Type (Teacher/Student)',
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        labels = {
            'text': 'Choice Text',
            'is_correct': 'Is Correct',
        }

class QuestionForm(forms.ModelForm):
    choices = forms.inlineformset_factory(
        Question,
        Choice,
        form=ChoiceForm,
        extra=4,  
        can_delete=False
    )

    class Meta:
        model = Question
        fields = ['text', 'difficulty']
        labels = {
            'text': 'Question Text',
            'difficulty': 'Difficulty Level',
        }