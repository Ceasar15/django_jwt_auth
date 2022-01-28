import email
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=55, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
        
    class Meta:
        ordering = ('username',)
        
    def __init__(self, token=None):
        self.toke = token
        
    def __str__(self):
        return self.username
