from django.contrib import admin
from .models import Account

# Административный интерфейс для управления банковскими счетами и картами в панеле Django Admin
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    # Колоки таблицы: название счета, владелец, баланс, валюта, дата создания
    list_display = ('name', 'user', 'balance', 'currency', 'created_at')
    
    # Правая панель фильтрации по валюте (UZS, USD, EUR) и дате добавления
    list_filter = ('currency', 'created_at')
    
    # Поиск по названию счета и логину пользователя
    search_fields = ('name', 'user__username')
