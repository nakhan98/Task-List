from django import forms
from django.contrib.auth.models import User
from models import Task

class UserForm(forms.ModelForm):
    """User registration form"""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class AddTaskForm(forms.ModelForm):
    """Form for adding a Task"""
    is_hidden = forms.BooleanField(widget=forms.RadioSelect(
        choices=[(True, '1'), (False, '0') ]), required=False)

    class Meta:
        model = Task
        fields = ("title", "description", "is_hidden")
