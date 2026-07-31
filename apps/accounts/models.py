from django.db import models
from django.conf import settings

class Account(models.Model):
    CURRENCY_CHOICES = [
        ('UZS', 'Oʻzbek soʻmi (UZS)'),
        ('USD', 'AQSH dollari (USD)'),
        ('EUR', 'Yevro (EUR)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100, verbose_name="Hisob nomi")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name="Balans")
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='UZS', verbose_name="Valyuta")
    icon = models.CharField(max_length=50, default='wallet', verbose_name="Ikonka")
    color = models.CharField(max_length=20, default='#4CAF50', verbose_name="Rang")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hisob"
        verbose_name_plural = "Hisoblar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency})"
