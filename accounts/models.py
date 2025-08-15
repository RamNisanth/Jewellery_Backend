from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission

# Owner table: handles login for the store owner
class Owner(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Fix the reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='owner_set',  # change from default user_set
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='owner_set',  # change from default user_set
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# Customer table: the end users who search or interact
class Customer(models.Model):
    id = models.AutoField(primary_key=True)  # primary key
    name = models.CharField(max_length=100)  # mandatory
    email = models.EmailField(unique=True)   # mandatory
    phone = models.CharField(max_length=20, blank=True)  # optional
    address = models.TextField(blank=True)  # optional

    def __str__(self):
        return self.name
