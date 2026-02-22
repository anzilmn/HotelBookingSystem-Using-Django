from django.contrib import admin
from .models import Room, Booking, Review

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'category', 'beds', 'capacity', 'price_per_night', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'check_in', 'check_out', 'status', 'total_cost']
    list_filter = ['status', 'check_in']
    actions = ['confirm_bookings', 'cancel_bookings']

    def confirm_bookings(self, request, queryset):
        queryset.update(status='CONFIRMED')
    
    def cancel_bookings(self, request, queryset):
        queryset.update(status='CANCELLED')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured']
    list_editable = ['is_featured'] # Fast-track reviews to homepage