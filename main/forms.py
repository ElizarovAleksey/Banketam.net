from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser, Booking
from django.utils import timezone
from datetime import datetime, time

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
    # Дата в формате ДД.ММ.ГГГГ 
    start_date = forms.CharField(label="Дата начала (ДД.ММ.ГГГГ)")

    class Meta:
        model = Booking
        fields = ['venue', 'start_date', 'payment_method']
        labels = {
            'venue': 'Выберите помещение',
            'payment_method': 'Способ оплаты',
        }

    def clean_start_date(self):
        value = self.cleaned_data['start_date'].strip()
        try:
            dt = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise forms.ValidationError("Введите дату в формате ДД.ММ.ГГГГ")
        return dt.date()

    def save(self, commit=True):
        obj = super().save(commit=False)
        # Время можно поставить фиксированное
        d = self.cleaned_data['start_date']
        obj.start_datetime = datetime.combine(d, time(18, 0))
        if commit:
            obj.save()
        return obj