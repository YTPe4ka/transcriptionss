from django.contrib import admin
from .models import Transaction

# Административный интерфейс для мониторинга и управления всеми транзакциями (расходами и доходами)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # Колонки таблицы операций: ID, пользователь, тип (расход/доход), сумма, счет, категория, дата
    list_display = ('id', 'user', 'type', 'amount', 'account', 'category', 'transaction_date', 'created_at')
    
    # Фильтры списка операций по типу транзакции, счету, категории и дате проведения
    list_filter = ('type', 'account', 'category', 'transaction_date')
    
    # Поиск по текстовому комментарию, логину владельца и названию счета
    search_fields = ('comment', 'user__username', 'account__name')
