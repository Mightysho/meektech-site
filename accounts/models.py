from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    ROLE_CHOICES = (
        ("CLIENT", "Client"),
        ("STAFF", "Staff"),
        ("INTERN", "Intern"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"