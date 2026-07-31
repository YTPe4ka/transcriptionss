from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    LANGUAGE_CHOICES = [
        ('uz', 'Oʻzbekcha'),
        ('ru', 'Русский'),
        ('en', 'English'),
    ]

    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    preferred_language = models.CharField(
        max_length=5, 
        choices=LANGUAGE_CHOICES, 
        default='uz', 
        verbose_name="Tanlangan til"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username or self.email
