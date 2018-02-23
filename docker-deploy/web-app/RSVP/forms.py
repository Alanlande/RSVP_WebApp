from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Role, Choice, Question

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'vendor_permission']

class editQuestionForm(forms.Form):
    question_text = forms.CharField(label="New Question Name", max_length=100)

class InviteForm(forms.Form):
    ROLE_CHOICES = (
    ("owner", ("owner")),
    ("vendor", ("vendor")),
    ("guest", ("guest")),
    )
    role = forms.ChoiceField(choices = ROLE_CHOICES, label="invite type", widget=forms.Select(), required=True)
    user_name = forms.CharField(label='user name', max_length=100)

class FinalizeForm(forms.Form):
    finalization = forms.BooleanField(label="finalize this question")

class TextForm(forms.Form):
    answer = forms.CharField(label="Free Text Answer here")

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class pendingForm(forms.Form):
    STATUS_CHOICES = (
        ("accept", ("accept")),
        ("deny", ("deny"))
    )
    status = forms.ChoiceField(choices = STATUS_CHOICES, label="status type", widget=forms.Select(), required=True)
