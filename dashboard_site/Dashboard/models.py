from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='dashboard_users')
    user_permissions = models.ManyToManyField(Permission, related_name='dashboard_users')

    def __str__(self):
        return f"Username: {self.username}"
    
class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    username = models.CharField(max_length=255) 
    password = models.CharField(max_length=255)
    followers = models.IntegerField(default=0)
