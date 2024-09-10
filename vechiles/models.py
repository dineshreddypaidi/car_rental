from django.db import models
from django.contrib.auth.models import User
import uuid
import random,string
from django.conf import settings
# Create your models here.

class Cars(models.Model):
    FUEL_TYPE_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]
    
    AVAILABILITY_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
        ('Reserved', 'Reserved'),
    ]
    
    TRANSMISSION_TYPES_CHOICES = [
        ('Automatic', 'Automatic'),
        ('Manual', ' Manual'),
        ('Semi-automatic', 'Semi-automatic')
    ]
    
    vechile_id = models.CharField(max_length=255,unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    plate_number = models.CharField(max_length=255,unique=True)
    description = models.TextField(default='')
    fuel_type = models.CharField(max_length=25, choices=FUEL_TYPE_CHOICES)
    availability_status = models.CharField(max_length=15, choices=AVAILABILITY_STATUS_CHOICES, default='Available')
    
    transmission_type = models.CharField(max_length=15, choices=TRANSMISSION_TYPES_CHOICES,default='Manual')
    seats = models.IntegerField(default=5)
    mileage = models.IntegerField(default=10)
    
    rental_rate_per_hour = models.IntegerField()
    rental_rate_per_day = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.plate_number
    
class Bikes(models.Model):
    FUEL_TYPE_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Electric', 'Electric'),
    ]
    
    AVAILABILITY_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
        ('Reserved', 'Reserved'),
    ]
    
    vechile_id = models.CharField(max_length=10,unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    plate_number = models.CharField(max_length=25,unique=True)
    description = models.TextField(default='')
    fuel_type = models.CharField(max_length=25, choices=FUEL_TYPE_CHOICES)
    availability_status = models.CharField(max_length=15, choices=AVAILABILITY_STATUS_CHOICES, default='Available')
    mileage = models.IntegerField(default=10)
    
    rental_rate_per_hour = models.IntegerField()
    rental_rate_per_day = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.plate_number
    
class carimages(models.Model):
    car = models.ForeignKey(Cars,on_delete=models.CASCADE)  
    image = models.ImageField(upload_to='car_images/',max_length=2000)
    
    def save(self, *args, **kwargs):
        super(carimages, self).save(*args, **kwargs)
        if self.image:
            self.image = f'{settings.MEDIA_URL}{self.image.name}'
            super(carimages, self).save(update_fields=['image'])
            
    def __str__(self):
        return f'{self.car}->{self.image}'
    
class bikeimages(models.Model):
    bike = models.ForeignKey(Bikes,on_delete=models.CASCADE)  
    image = models.ImageField(upload_to='bike_images/',max_length=2000)      
    
    def save(self, *args, **kwargs):
        super(bikeimages, self).save(*args, **kwargs)
        if self.image:
            self.image = f'{settings.MEDIA_URL}{self.image.name}'
            super(bikeimages, self).save(update_fields=['image'])
            
    def __str__(self):
        return f'{self.bike}->{self.image}'
   
def generate_booking_id(username, vehicle_name):
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        booking_id = f"{username}-{vehicle_name}-{random_string}"
        return booking_id
       
class carBooking(models.Model):
    RENTAL_STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('In Progress', 'In Progress'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
       
    booking_id = models.CharField(max_length=30, editable=False, default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    vechile = models.ForeignKey(Cars,on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=15, choices=RENTAL_STATUS_CHOICES, default='Confirmed')
    
    is_active = models.BooleanField(default=True)
    rent_start_date = models.DateTimeField(null=True,blank=True)
    rent_end_date = models.DateTimeField(null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = generate_booking_id(self.user.username, self.vechile.vechile_id)
        super(carBooking, self).save(*args, **kwargs)

    def __str__(self):
        return self.booking_id
    
class bikeBooking(models.Model):
    RENTAL_STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('In Progress', 'In Progress'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    
    booking_id = models.CharField(max_length=30, editable=False, default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    vechile = models.ForeignKey(Bikes,on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=15, choices=RENTAL_STATUS_CHOICES, default='Confirmed')
    
    is_active = models.BooleanField(default=True)
    rent_start_date = models.DateTimeField(null=True,blank=True)
    rent_end_date = models.DateTimeField(null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = generate_booking_id(self.user.username, self.vechile.vechile_id)
        super(bikeBooking, self).save(*args, **kwargs)

    def __str__(self):
        return self.booking_id
    
class carReview(models.Model):
    RATING_CHOICES = [
        (i, str(i)) for i in range(1, 6)
        ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Cars, on_delete=models.CASCADE)
    booking_id = models.ForeignKey(carBooking, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.booking_id} - {self.rating}'
    
class bikeReview(models.Model):
    RATING_CHOICES = [
        (i, str(i)) for i in range(1, 6)
        ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Bikes, on_delete=models.CASCADE)
    booking_id = models.ForeignKey(bikeBooking, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.booking_id} - {self.rating}'
    
class car_stats(models.Model):
    car = models.ForeignKey(Cars,on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    rentals = models.PositiveIntegerField(default=0)
    earned = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    average_user_rating = models.FloatField(default=0.0)
    
class bike_stats(models.Model):
    car = models.ForeignKey(Bikes,on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    rentals = models.PositiveIntegerField(default=0)
    earned = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    average_user_rating = models.FloatField(default=0.0)