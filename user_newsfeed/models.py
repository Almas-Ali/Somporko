from django.db import models
from django.utils.timezone import now
# Create your models here.

class Announcement(models.Model):
    admin = models.CharField(max_length=100, default='Admin')
    text = models.TextField(max_length=5000, default='')
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.admin
    
