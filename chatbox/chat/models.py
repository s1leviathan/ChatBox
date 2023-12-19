from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.ManyToManyField(Users)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"