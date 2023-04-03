from django.db import models


# Create your models here.
class UserToken(models.Model):
    token = models.CharField(max_length=1000)
    deviceId = models.CharField(max_length=500, primary_key=True)
    isActive = models.BooleanField(default=True)
    address = models.CharField(max_length=1000, default="")
    phoneNumber = models.CharField(max_length=20, default="")
    name = models.CharField(max_length=500, default="")
    email = models.CharField(max_length=300, default="")
    password = models.CharField(max_length=300, default="")
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.deviceId
