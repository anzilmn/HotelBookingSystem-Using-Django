from django.urls import path
from .views import RoomListView, RoomDetailView, manager_dashboard,download_receipt,MyBookingsView,cancel_booking

app_name = 'booking'

urlpatterns = [
    path('', RoomListView.as_view(), name='RoomList'),  # Set as home page
    path('room/<int:pk>/', RoomDetailView.as_view(), name='RoomDetail'),
    path('dashboard/', manager_dashboard, name='manager_dashboard'),
    path('booking/<int:booking_id>/receipt/', download_receipt, name='download_receipt'),
    path('my-bookings/', MyBookingsView.as_view(), name='MyBookings'),
path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
path('download-receipt/<int:booking_id>/', download_receipt, name='download_receipt'),
]