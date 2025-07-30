from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
   
    number = models.CharField(max_length=64, unique=True)
    type = models.CharField(max_length=6420, choices=[('apartment', 'Apartment'), ('house', 'House')])
    price = models.DecimalField(max_digits=64, decimal_places=2)
    is_available = models.BooleanField(default=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    rooms_count = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(help_text='Size in m²', default=0)
    floors = models.PositiveIntegerField(default=1)

    def get_type_display_ua(self):
       
        return {'apartment': 'Квартира', 'house': 'Дім'}.get(self.type, self.type)

    def __str__(self):
        
        return f"Room {self.number} ({self.get_type_display()})"

class RoomPhoto(models.Model):
   
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='room_photos/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return f"Photo for Room {self.room.number}"

class Booking(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)

    @property
    def nights(self):
       
        return (self.check_out_date - self.check_in_date).days

    @property
    def total_price(self):
        
        return self.nights * self.room.price

    def __str__(self):
       
        return f"Booking by {self.user.username} for Room {self.room.number}"
