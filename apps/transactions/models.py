from django.db import models, transaction as db_transaction
from django.conf import settings
from django.utils import timezone
from apps.accounts.models import Account
from apps.categories.models import Category

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('EXPENSE', 'Chiqim'),
        ('INCOME', 'Kirim'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', verbose_name="Hisob")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions', verbose_name="Kategoriya")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='EXPENSE', verbose_name="Operatsiya turi")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Summa")
    transaction_date = models.DateField(default=timezone.now, verbose_name="Sana")
    comment = models.TextField(blank=True, null=True, verbose_name="Izoh")
    photo = models.ImageField(upload_to='transactions/', blank=True, null=True, verbose_name="Rasm")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tranzaksiya"
        verbose_name_plural = "Tranzaksiyalar"
        ordering = ['-transaction_date', '-created_at']

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} {self.account.currency} ({self.transaction_date})"

    @db_transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_transaction = None
        if not is_new:
            old_transaction = Transaction.objects.get(pk=self.pk)

        super().save(*args, **kwargs)

        # Balance adjustment logic
        if is_new:
            if self.type == 'EXPENSE':
                self.account.balance -= self.amount
            else:
                self.account.balance += self.amount
            self.account.save(update_fields=['balance'])
        else:
            # Revert old transaction balance impact
            if old_transaction.type == 'EXPENSE':
                old_transaction.account.balance += old_transaction.amount
            else:
                old_transaction.account.balance -= old_transaction.amount
            old_transaction.account.save(update_fields=['balance'])

            # Refresh current account in case it changed
            account = Account.objects.get(pk=self.account.pk)
            if self.type == 'EXPENSE':
                account.balance -= self.amount
            else:
                account.balance += self.amount
            account.save(update_fields=['balance'])

    @db_transaction.atomic
    def delete(self, *args, **kwargs):
        # Revert balance on deletion
        if self.type == 'EXPENSE':
            self.account.balance += self.amount
        else:
            self.account.balance -= self.amount
        self.account.save(update_fields=['balance'])
        super().delete(*args, **kwargs)
