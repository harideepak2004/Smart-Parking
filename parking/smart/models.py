from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CompanyDetail(models.Model):
    FLOOR_CHOICES = [
        ('GRND', 'Ground Floor'),
        ('F01', '1 Floor'),
        ('F02', '2 Floor'),
        ('F03', '3 Floor'),
        ('F04', '4 Floor'),
        ('F05', '5 Floor'),
        ('F06', '6 Floor'),
        ('F07', '7 Floor'),
        ('F08', '8 Floor'),
        ('F09', '9 Floor'),
        ('F10', '10 Floor'),
        ('F11', '11 Floor'),
        ('F12', '12 Floor'),
    ]

    SLOT_CHOICES = [
        ('S01', '1 Slot'),
        ('S02', '2 Slots'),
        ('S03', '3 Slots'),
        ('S04', '4 Slots'),
        ('S05', '5 Slots'),
        ('S06', '6 Slots'),
        ('S07', '7 Slots'),
        ('S08', '8 Slots'),
        ('S09', '9 Slots'),
        ('S10', '10 Slots'),
        ('S11', '11 Slots'),
        ('S12', '12 Slots'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    floors = models.CharField(max_length=4, choices=FLOOR_CHOICES)
    slots = models.CharField(max_length=4, choices=SLOT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name


class ParkingUser(models.Model):
    name = models.CharField(max_length=100)
    car_number = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    slot = models.CharField(max_length=20, default="Not Assigned")
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)     # ✅ NEW
    is_active = models.BooleanField(default=True)
    price_per_hour = models.FloatField(default=50)  # Rs.50 per hour


    def __str__(self):
        return f"{self.name} - {self.car_number}"

