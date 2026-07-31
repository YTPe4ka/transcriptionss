from django.contrib import admin
from .models import Category

# Административный интерфейс для управления категориями расходов и доходов в панели Django Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Отображаемые колонки списка категорий (названия на 3 языках, тип EXPENSE/INCOME, пользователь, иконка, цвет)
    list_display = ('name_uz', 'name_ru', 'name_en', 'type', 'user', 'icon', 'color')
    
    # Боковая панель быстрых фильтров (по типу операции и пользователю)
    list_filter = ('type', 'user')
    
    # Поля поиска по названиям категорий на трех языках
    search_fields = ('name_uz', 'name_ru', 'name_en')
