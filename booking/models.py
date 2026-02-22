from django.db import models
from django.conf import settings
from django.urls import reverse

class Room(models.Model):
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    beds = models.IntegerField()
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Room {self.number} - {self.get_category_display()}'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    booked_on = models.DateTimeField(auto_now_add=True)
    
    # Status to allow admin to approve/reject
    status_choices = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

    def __str__(self):
        return f'{self.user} booked {self.room} from {self.check_in} to {self.check_out}'

    # Simple logic to calculate total price
    @property
    def total_cost(self):
        days = (self.check_out - self.check_in).days
        return days * self.room.price_per_night
    

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Review - {self.rating} Stars"    