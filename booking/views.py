from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from xhtml2pdf import pisa
from io import BytesIO

from .models import Room, Review, Booking
from .forms import AvailabilityForm, ReviewForm

# 1. PREMIUM HOME PAGE WITH MULTI-FILTERS
class RoomListView(ListView):
    model = Room
    template_name = 'booking/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by Category (AC/Non-AC/Deluxe/King)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        # Filter by Max Price (Slider)
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
            
        # Filter by Capacity (Guests count)
        capacity = self.request.GET.get('capacity')
        if capacity:
            queryset = queryset.filter(capacity__gte=capacity)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch featured reviews for the bottom section
        context['reviews'] = Review.objects.filter(is_featured=True)[:3]
        
        # Pass current filters back to template to keep the form state (Sticky Inputs)
        context['current_category'] = self.request.GET.get('category', '')
        context['current_max_price'] = self.request.GET.get('max_price', '1000')
        context['current_capacity'] = self.request.GET.get('capacity', '1')
        return context

# 2. ROOM DETAIL, BOOKING & REVIEW LOGIC
class RoomDetailView(View):
    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        form = AvailabilityForm()
        review_form = ReviewForm()
        reviews = Review.objects.filter(room=room).order_by('-created_at')
        return render(request, 'booking/room_detail.html', {
            'room': room, 
            'form': form, 
            'review_form': review_form,
            'reviews': reviews
        })

    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        reviews = Review.objects.filter(room=room).order_by('-created_at')
        
        # ACTION 1: Handle Review Submission
        if 'submit_review' in request.POST:
            if not request.user.is_authenticated:
                return redirect('login')
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.room = room
                review.user = request.user
                review.save()
                return redirect('booking:RoomDetail', pk=pk)
            return render(request, 'booking/room_detail.html', {
                'room': room, 'form': AvailabilityForm(), 'review_form': review_form, 'reviews': reviews
            })

        # ACTION 2: Handle Booking Submission
        form = AvailabilityForm(request.POST)
        review_form = ReviewForm()
        if form.is_valid():
            data = form.cleaned_data
            booking_list = Booking.objects.filter(room=room)
            
            # Check for date overlaps
            is_available = not booking_list.filter(
                check_in__lt=data['check_out'],
                check_out__gt=data['check_in']
            ).exclude(status='CANCELLED').exists()

            if is_available:
                if request.user.is_authenticated:
                    # WE CREATE AND CAPTURE THE BOOKING HERE
                    new_booking = Booking.objects.create(
                        user=request.user,
                        room=room,
                        check_in=data['check_in'],
                        check_out=data['check_out']
                    )
                    # Pass new_booking to context so "Download Receipt" link works immediately
                    return render(request, 'booking/room_detail.html', {
                        'room': room, 
                        'success': True, 
                        'booking': new_booking, # Important!
                        'reviews': reviews
                    })
                else:
                    return redirect('login')
            else:
                error = 'Vro, someone beat you to it! This room is booked for those dates.'
                return render(request, 'booking/room_detail.html', {
                    'room': room, 'form': form, 'review_form': review_form, 'error': error, 'reviews': reviews
                })
        
        return render(request, 'booking/room_detail.html', {
            'room': room, 'form': form, 'review_form': review_form, 'reviews': reviews
        })

# 3. MANAGER DASHBOARD
@staff_member_required
def manager_dashboard(request):
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    confirmed_bookings = Booking.objects.filter(status='CONFIRMED')
    total_revenue = sum(b.total_cost for b in confirmed_bookings)
    
    rooms = Room.objects.all()
    context = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'total_revenue': total_revenue,
        'rooms': rooms,
    }
    return render(request, 'booking/manager_dashboard.html', context)

# 4. DOWNLOAD PDF RECEIPT
def download_receipt(request, booking_id):
    # Ensure only the owner of the booking can download the receipt
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    template = get_template('booking/receipt_pdf.html')
    html = template.render({'booking': booking})
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="StayEase_Receipt_{booking.id}.pdf"'
        return response
    return HttpResponse("Error generating PDF, vro!", status=400)




from django.contrib import messages

# 5. USER CANCEL BOOKING
def cancel_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        # Only allow cancellation if it's not already cancelled
        if booking.status != 'CANCELLED':
            booking.status = 'CANCELLED'
            booking.save()
            messages.success(request, f"Booking for Room {booking.room.number} has been cancelled.")
        else:
            messages.warning(request, "This booking is already cancelled.")
            
    return redirect('booking:MyBookings')

# 6. MY BOOKINGS VIEW (Ensure this exists to serve the template)
class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/my_bookings.html'
    context_object_name = 'bookings' # Matches your template loop {% for booking in bookings %}

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-check_in')