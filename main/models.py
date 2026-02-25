from django.db import models
from django.contrib.auth.models import AbstractUser


# ===============================
# модель пользователя
# ===============================
# Наследуемся от AbstractUser, чтобы расширить стандартную модель Django
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name="Контактный номер телефона")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


# ===============================
# Модель помещения для банкета
# ===============================
class Venue(models.Model):

    # Типы помещений
    TYPE_CHOICES = [
        ('hall', 'Зал'),
        ('restaurant', 'Ресторан'),
        ('summer', 'Летняя веранда'),
        ('closed', 'Закрытая веранда'),
    ]

    # Название помещения
    name = models.CharField(
        max_length=100,
        verbose_name="Название помещения"
    )

    # Тип помещения (выбор из списка)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Тип помещения"
    )

    # Адрес помещения
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес"
    )

    # Вместимость
    capacity = models.IntegerField(
        verbose_name="Вместимость (чел.)"
    )

    # Описание
    description = models.TextField(
        verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"

    def __str__(self):
        return self.name


# ===============================
# Модель заявки на бронирование
# ===============================
class Booking(models.Model):

    # Возможные статусы заявки
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Банкет назначен'),
        ('completed', 'Банкет завершен'),
    ]

    # Способы оплаты
    PAYMENT_CHOICES = [
        ('card', 'Карта'),
        ('cash', 'Наличные'),
        ('transfer', 'Перевод'),
    ]

    # Пользователь, создавший заявку
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    # Выбранное помещение
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        verbose_name="Помещение"
    )

    # Дата и время начала банкета
    start_datetime = models.DateTimeField(
        verbose_name="Дата и время начала"
    )

    # Способ оплаты
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name="Способ оплаты"
    )

    # Статус заявки (по умолчанию "Новая")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )

    # Дата создания заявки
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
        
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка #{self.id} — {self.user.username}"


# ===============================
# Модель отзыва
# ===============================
class Review(models.Model):

    # Автор отзыва
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    # Одна заявка = один отзыв
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        verbose_name="Заявка"
    )

    # Оценка от 1 до 5
    rating = models.IntegerField(
        verbose_name="Оценка"
    )

    # Текст отзыва
    text = models.TextField(
        verbose_name="Текст отзыва"
    )

    # Дата создания
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв пользователя {self.user.username}"