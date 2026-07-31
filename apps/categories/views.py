from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Category
from .serializers import CategorySerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

# CRUD ViewSet для работы с категориями расходов и доходов
@extend_schema_view(
    list=extend_schema(
        summary="Kategoriyalar roʻyxati (Kirim/Chiqim)",
        parameters=[
            OpenApiParameter(name='type', description='EXPENSE yoki INCOME boʻyicha saralash', required=False, type=str),
            OpenApiParameter(name='lang', description='Til kodi: uz, ru, en (Default: uz)', required=False, type=str),
        ],
        tags=["Kategoriyalar"]
    ),
    create=extend_schema(summary="Yangi kategoriya yaratish", tags=["Kategoriyalar"]),
    retrieve=extend_schema(summary="Kategoriya tafsilotlari", tags=["Kategoriyalar"]),
    update=extend_schema(summary="Kategoriyani tahrirlash", tags=["Kategoriyalar"]),
    destroy=extend_schema(summary="Kategoriyani oʻchirish", tags=["Kategoriyalar"]),
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    # Метод фильтрации категорий: возвращает системные дефолтные категории + персональные категории пользователя
    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.filter(Q(user=user) | Q(user__isnull=True))
        
        # Дополнительная фильтрация по типу операции: EXPENSE (расход) или INCOME (доход)
        category_type = self.request.query_params.get('type')
        if category_type in ['EXPENSE', 'INCOME']:
            queryset = queryset.filter(type=category_type)
            
        return queryset

    # Автоматически привязывает новую категорию к создавшему ее пользователю
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
