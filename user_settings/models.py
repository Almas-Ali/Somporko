from django.db import models
from django.utils.timezone import now
from user_profiles.models import User


class UserPrivacy(models.Model):
    hide_email = models.CharField(max_length=10, default='No')
    hide_phone = models.CharField(max_length=10, default='No')
    hide_friends = models.CharField(max_length=10, default='No')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, blank=False)

    def __str__(self):
        return str(self.user)
    
class Delete_Request(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, blank=False)
    email = models.CharField(max_length=100, default='')
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.user
    
class VerifyUser(models.Model):
    is_verified = models.CharField(default='No', max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
    
