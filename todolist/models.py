from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Models for todolist
#we need a mdoel for our todo. Fields: title, optional:(notes), important?, due by:, 

class Todo(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    title= models.CharField(max_length=100)
    notes = models.CharField(max_length=255, blank=True)
    important = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    due_by = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos", blank=True, null=True)

