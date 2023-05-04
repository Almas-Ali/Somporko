from django.db import models


class Home_About(models.Model):
    title = models.CharField(max_length=100, default='')
    desc = models.TextField(max_length=10000, default='')

    def __str__(self):
        return self.title

class Report(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=25)
    phone = models.CharField(max_length=14)
    msg = models.TextField(max_length=500)
    date = models.DateTimeField()

    def __str__(self):
        return self.name