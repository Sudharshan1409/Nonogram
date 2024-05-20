from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', required=True)
    name = forms.CharField(label='Full Name', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2:
            raise forms.ValidationError("One of the Passwords fields are empty")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        name = cleaned_data.get('name')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if not email:
            raise forms.ValidationError("Email is required")
        if not name:
            raise forms.ValidationError("First Name is required")
        if not password1 or not password2:
            raise forms.ValidationError("One of the Passwords fields are empty")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username or Email'
        self.fields['password'].label = 'Password'

