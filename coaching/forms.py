from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from .models import *

#//////////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(label='Email' , validators=[EmailValidator],error_messages={"invalid email":"try again"})
    # first_name = forms.CharField(label="First Name")
    # last_name = forms.CharField(label="Last Name")
    class Meta:
        model = User
        fields = ['username','email']


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user','status')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'