from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser, Booking


# =====================================
# Форма регистрации пользователя
# =====================================
class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'email', 'phone', 'password1', 'password2']
        labels = {
            'username': 'Логин',
            'first_name': 'ФИО',
            'email': 'E-mail',
            'phone': 'Телефон',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    # Проверка логина: латиница + цифры, минимум 6 символов
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[A-Za-z0-9]{6,}$', username):
            raise ValidationError("Логин должен содержать минимум 6 латинских букв или цифр.")
        return username


# =====================================
# Форма создания заявки
# =====================================
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['venue', 'start_datetime', 'payment_method']
        labels = {
            'venue': 'Выберите помещение',
            'start_datetime': 'Дата и время начала',
            'payment_method': 'Способ оплаты',
        }
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }