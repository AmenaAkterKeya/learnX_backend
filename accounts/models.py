from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=300 ,null=True, blank=True)
    mobile_no = models.CharField(max_length = 12)
    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=300 ,null=True, blank=True)
    mobile_no = models.CharField(max_length = 12)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
