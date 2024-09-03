from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UploadedFile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.content_type != 'application/pdf':
                raise forms.ValidationError('Only PDF files are allowed.')
        return file

class PaperSubmissionForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'user_name', 'domain', 'file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['reviewer_comment']
