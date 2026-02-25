from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cabinet/', views.cabinet_view, name='cabinet'),
    path('booking/create/', views.create_booking_view, name='create_booking'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('admin-panel/update/<int:booking_id>/<str:new_status>/', 
     views.update_booking_status, 
     name='update_booking_status'),
    path('booking/<int:booking_id>/review/', views.add_review_view, name='add_review'),
]