from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None  # Удаляем помощь по каждому полю

    def non_field_errors(self):
        errors = []
        for field in self.errors:
            if field != '__all__':  # Исключаем ошибки для всех полей
                for error in self.errors[field]:
                    errors.append(error)
        return errors

    def errors_as_text(self):
        errors = self.non_field_errors()
        if errors:
            return '\n'.join(errors)
        return ''
