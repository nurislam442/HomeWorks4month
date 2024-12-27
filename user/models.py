from django.db import models
from django.contrib.auth.models import User

 
class Profile(models.Model):
    image = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username