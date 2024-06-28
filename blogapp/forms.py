from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.template.defaulttags import comment

from blogapp.models import Profile, Post, Category, Tag


class UserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'id_password'}),
        required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'id': "id_password_confirm"}), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'id_username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'id_email'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name', 'id': 'id_firstname'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name', 'id': 'id_lastname'}),
        }

        def clean_password_confirm(self):
            password = self.cleaned_data.get('password1')
            password_confirm = self.cleaned_data.get('password2')
            if password and password_confirm and password != password_confirm:
                raise forms.ValidationError("Passwords don't match")
            return password_confirm


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'id_username'}),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'id_password'}),
        required=True)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bio', 'id': 'id_bio'}),
        }


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': 'multiple', 'onchange': "jsFunction();"}),
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': 'multiple'}),
        required=False
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'categories', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'id': 'id_title'}),
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Content', 'id': 'id_content'}),
        }

        def save(self, commit=True):
            instance = super().save(commit=False)
            if commit:
                instance.save()
                self.save_m2m()
            return instance
