from collections import deque
from pyexpat import model
from tkinter import CASCADE
from turtle import title
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    description=models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Notes'
        verbose_name_plural = 'Notes'


class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    description=models.TextField()
    due=models.DateTimeField()
    is_finish=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'homework'
        verbose_name_plural = 'homework'



class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.TextField()
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.title


