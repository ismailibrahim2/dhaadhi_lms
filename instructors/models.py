from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='instructors')
    qualification = models.CharField(max_length=300)
    mobile_phone = models.CharField(max_length=40)
    about = models.TextField()

    def __str__(self):
        return self.user.username
