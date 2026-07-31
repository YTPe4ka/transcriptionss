from rest_framework import viewsets, permissions
from .models import Account
from .serializers import AccountSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

# CRUD ViewSet для управления банковскими счетами и картами
@extend_schema_view(
    list=extend_schema(summary="Foydalanuvchi hisoblari roʻyxati", tags=["Hisoblar"]),
    create=extend_schema(summary="Yangi hisob yaratish (Naqd, Karta, Valyuta...)", tags=["Hisoblar"]),
    retrieve=extend_schema(summary="Hisob tafsilotlari", tags=["Hisoblar"]),
    update=extend_schema(summary="Hisobni tahrirlash", tags=["Hisoblar"]),
    destroy=extend_schema(summary="Hisobni oʻchirish", tags=["Hisoblar"]),
)
class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Метод фильтрует счета в БД, возвращая ТОЛЬКО счета текущего авторизованного пользователя
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    # Автоматически привязывает создаваемый счет к текущему вошедшему пользователю
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
