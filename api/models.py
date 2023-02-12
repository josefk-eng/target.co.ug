from django.db import models


# Create your models here.
class UserToken(models.Model):
    token = models.CharField(max_length=1000)
    deviceId = models.CharField(max_length=500)
    isActive = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.deviceId
