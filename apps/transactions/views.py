from rest_framework import viewsets, permissions
from .models import Transaction
from .serializers import TransactionSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

# CRUD ViewSet для управления транзакциями (расходами и доходами)
@extend_schema_view(
    list=extend_schema(
        summary="Foydalanuvchi tranzaksiyalari (Kirim va Chiqimlar roʻyxati)",
        parameters=[
            OpenApiParameter(name='type', description='Tranzaksiya turi: EXPENSE yoki INCOME', required=False, type=str),
            OpenApiParameter(name='account_id', description='Hisob ID boʻyicha filter', required=False, type=int),
            OpenApiParameter(name='category_id', description='Kategoriya ID boʻyicha filter', required=False, type=int),
            OpenApiParameter(name='start_date', description='Boshlanish sanasi (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='end_date', description='Tugash sanasi (YYYY-MM-DD)', required=False, type=str),
        ],
        tags=["Tranzaksiyalar"]
    ),
    create=extend_schema(summary="Yangi kirim/chiqim amali yaratish", tags=["Tranzaksiyalar"]),
    retrieve=extend_schema(summary="Tranzaksiya tafsiloti", tags=["Tranzaksiyalar"]),
    update=extend_schema(summary="Tranzaksiyani tahrirlash", tags=["Tranzaksiyalar"]),
    destroy=extend_schema(summary="Tranzaksiyani oʻchirish", tags=["Tranzaksiyalar"]),
)
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Метод формирования выборки транзакций с гибкой фильтрацией
    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(user=user).select_related('account', 'category')

        # Фильтр по типу операции (EXPENSE / INCOME)
        tx_type = self.request.query_params.get('type')
        if tx_type in ['EXPENSE', 'INCOME']:
            queryset = queryset.filter(type=tx_type)

        # Фильтр по конкретному счету/карте
        account_id = self.request.query_params.get('account_id')
        if account_id:
            queryset = queryset.filter(account_id=account_id)

        # Фильтр по категории расходов/доходов
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Фильтр по начальной дате
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)

        # Фильтр по конечной дате
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)

        return queryset

    # Автоматически проставляет текущего пользователя владельцем при создании транзакции
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
