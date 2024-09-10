from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

#auditlog
class AuditLog(models.Model):
    def default_record_id():
        import datetime
        current_time = datetime.datetime.now()
        return f'{current_time.year}{current_time.month}{current_time.day}'
    
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=255)
    record_id = models.CharField(max_length=255,default=default_record_id())
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} - {self.action} -->{self.timestamp}"
    
    
class promotion(models.Model):
    name = models.CharField(max_length=30)
    promotion_text = models.TextField()
    is_active = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.promotion_text}"
    
class contact(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.name