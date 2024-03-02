import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=50)
    task_description = models.TextField(max_length=255, null=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField()

