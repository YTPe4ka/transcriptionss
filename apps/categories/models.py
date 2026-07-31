from django.db import models
from django.conf import settings

class Category(models.Model):
    TYPE_CHOICES = [
        ('EXPENSE', 'Chiqim'),
        ('INCOME', 'Kirim'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='categories',
        null=True, 
        blank=True,
        help_text="Null boʻlsa barcha foydalanuvchilar uchun umumiy (default) kategoriya hisoblanadi."
    )
    name_uz = models.CharField(max_length=100, verbose_name="Nomi (Oʻzbekcha)")
    name_ru = models.CharField(max_length=100, verbose_name="Nomi (Ruscha)")
    name_en = models.CharField(max_length=100, verbose_name="Nomi (Inglizcha)")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='EXPENSE', verbose_name="Turi")
    icon = models.CharField(max_length=50, default='grid', verbose_name="Ikonka")
    color = models.CharField(max_length=20, default='#3F51B5', verbose_name="Rang")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['type', 'id']

    def get_name(self, lang='uz'):
        if lang == 'ru':
            return self.name_ru or self.name_uz
        elif lang == 'en':
            return self.name_en or self.name_uz
        return self.name_uz

    def __str__(self):
        return f"{self.name_uz} ({self.get_type_display()})"
