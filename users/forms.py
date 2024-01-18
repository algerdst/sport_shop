from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Фамилия пользователя'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Адрес доставки'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'address', 'email', 'password1', 'password2']


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'placeholder': 'Изображение'}), required=False)
    address = forms.ImageField(widget=forms.TextInput, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'address', 'image']

# class Address_Form(forms.Form):
#     address=forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'address_form', 'placeholder': 'Введите адрес доставки'
#     }))
