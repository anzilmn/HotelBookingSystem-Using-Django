from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from booking.models import Booking

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('booking:RoomList')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})




from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'CANCELLED':
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.info(request, "Booking is already cancelled.")
        
    return redirect('my_bookings')