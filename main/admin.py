from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Venue, Booking, Review


# Регистрация кастомного пользователя в админке
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


# Регистрация остальных моделей
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity')
    search_fields = ('name', 'address')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'venue', 'status', 'start_datetime')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'rating')