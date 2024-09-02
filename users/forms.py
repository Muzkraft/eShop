from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password']
    
    username = forms.CharField() # так как в классе AuthenticationForm данные поля присутствуют, то их можно и не объявлять
    password = forms.CharField() # так как в классе AuthenticationForm данные поля присутствуют, то их можно и не объявлять
    
    ### login form var_2 ###
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "autofocus": True,
    #             "class": "form-control",
    #             "placeholder": "Введите имя пользователя",
    #         }
    #     )
    # )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "autocomplete": "current-password",
    #             "class": "form-control",
    #             "placeholder": "Введите ваш пароль",
    #         }
    #     )
    # )

class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        )
        
        first_name = forms.CharField()
        last_name = forms.CharField()
        username = forms.CharField()
        email = forms.CharField()
        password1 = forms.CharField()
        password2 = forms.CharField()