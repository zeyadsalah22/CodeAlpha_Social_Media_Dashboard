from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='dashboard_users')
    user_permissions = models.ManyToManyField(Permission, related_name='dashboard_users')

    def __str__(self):
        return f"Username: {self.username}"
