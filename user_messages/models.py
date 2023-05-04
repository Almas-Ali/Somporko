from django.db import models
# from django.contrib.auth.models import User
from django.utils.timezone import now
from user_profiles.models import User

# Create your models here.


class UserMessages(models.Model):
    id = models.AutoField(primary_key=True)
    msg = models.TextField(default='', max_length=5000)
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)
    ip = models.CharField(max_length=15, default='')
    time = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.from_user)
