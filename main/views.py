from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, BookingForm
from .models import Booking



# ===============================
# Регистрация
# ===============================
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cabinet')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# ===============================
# Авторизация
# ===============================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cabinet')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# ===============================
# Выход
# ===============================
def logout_view(request):
    logout(request)
    return redirect('login')


# ===============================
# Личный кабинет
# ===============================
@login_required
def cabinet_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'cabinet.html', {'bookings': bookings})


# ===============================
# Создание заявки
# ===============================
@login_required
def create_booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('cabinet')
    else:
        form = BookingForm()

    return render(request, 'create_booking.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test
from .models import Booking


# Проверка: пользователь — администратор
def is_admin(user):
    return user.is_authenticated and user.username == "Admin26"


# Панель администратора
@user_passes_test(is_admin)
def admin_panel_view(request):
    qs = Booking.objects.select_related('user', 'venue').all()

    # Фильтры
    status = request.GET.get('status', '').strip()
    venue_id = request.GET.get('venue', '').strip()

    if status:
        qs = qs.filter(status=status)
    if venue_id.isdigit():
        qs = qs.filter(venue_id=int(venue_id))

    # Сортировка
    order = request.GET.get('order', '-created_at')
    allowed = {'created_at', '-created_at', 'start_datetime', '-start_datetime', 'status', '-status'}
    if order not in allowed:
        order = '-created_at'
    qs = qs.order_by(order)

    # Пагинация
    paginator = Paginator(qs, 10)  # по 10 записей
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    from .models import Venue
    venues = Venue.objects.all()

    return render(request, 'admin_panel.html', {
        'page_obj': page_obj,
        'venues': venues,
        'status': status,
        'venue_id': venue_id,
        'order': order,
    })


# Изменение статуса заявки
@user_passes_test(is_admin)
def update_booking_status(request, booking_id, new_status):
    booking = Booking.objects.get(id=booking_id)
    booking.status = new_status
    booking.save()
    messages.success(request, f"Статус заявки #{booking.id} изменён.")
    return redirect('admin_panel')

from .models import Review
from django.shortcuts import get_object_or_404

# Отзыв
@login_required
def add_review_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Проверяем, завершён ли банкет
    if booking.status != 'completed':
        return redirect('cabinet')

    # Проверяем, нет ли уже отзыва
    if hasattr(booking, 'review'):
        return redirect('cabinet')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        Review.objects.create(
            user=request.user,
            booking=booking,
            rating=rating,
            text=text
        )

        return redirect('cabinet')

    return render(request, 'add_review.html', {'booking': booking})