from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Административный интерфейс для управления пользователями системы
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Колонки таблицы пользователей: логин, email, имя, фамилия, предпочитаемый язык, статус персонала
    list_display = ('username', 'email', 'first_name', 'last_name', 'preferred_language', 'is_staff')
    
    # Дополнительные группы полей в форме просмотра и редактирования аккаунта
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qoʻshimcha maʼlumotlar', {'fields': ('phone_number', 'preferred_language')}),
    )
