from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class userprofile(models.Model):
    MEMBERSHIP_CHOICES = [
        ('Silver','Silver'),
        ('Gold','Gold'),
        ('Platinum','Platinum'),
        ('Diamond','Diamond'),
    ]
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    no_of_bookings = models.IntegerField(default=0)
    member_ship = models.CharField(max_length=10,choices=MEMBERSHIP_CHOICES,default='Silver')
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username.username