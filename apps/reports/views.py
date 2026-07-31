from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from apps.transactions.models import Transaction
from apps.accounts.models import Account
from apps.categories.models import Category
from drf_spectacular.utils import extend_schema, OpenApiParameter
from decimal import Decimal

# Вспомогательная функция вычисления диапазона дат по переданному периоду (день, неделя, месяц, год, произвольный период)
def get_date_range(period, start_date_str=None, end_date_str=None):
    today = timezone.now().date()
    if period == 'day':
        return today, today
    elif period == 'week':
        start = today - timedelta(days=today.weekday())
        return start, today
    elif period == 'month':
        start = today.replace(day=1)
        return start, today
    elif period == 'year':
        start = today.replace(month=1, day=1)
        return start, today
    elif period == 'period' or period == 'custom':
        if start_date_str and end_date_str:
            try:
                start = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                return start, end
            except ValueError:
                pass
    return today.replace(day=1), today

# Класс отчета общей сводки финансов (Общий баланс, Доходы, Расходы, Сбережения)
class SummaryReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Umumiy hisobot va balans balansi",
        parameters=[
            OpenApiParameter(name='period', description='Davr: day, week, month, year, period', required=False, type=str),
            OpenApiParameter(name='start_date', description='Boshlanish sanasi (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='end_date', description='Tugash sanasi (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='account_id', description='Hisob ID', required=False, type=int),
        ],
        tags=["Hisobotlar"]
    )
    # Метод обработки GET запроса сводного отчета
    def get(self, request):
        user = request.user
        period = request.query_params.get('period', 'month')
        start_date, end_date = get_date_range(
            period, 
            request.query_params.get('start_date'), 
            request.query_params.get('end_date')
        )

        # Выборка счетов пользователя (с опциональным фильтром по конкретной карте)
        accounts_qs = Account.objects.filter(user=user)
        account_id = request.query_params.get('account_id')
        if account_id:
            accounts_qs = accounts_qs.filter(id=account_id)

        # Суммирование общего баланса
        total_balance = Decimal(accounts_qs.aggregate(total=Sum('balance'))['total'] or 0)

        # Выборка транзакций за диапазон дат
        tx_qs = Transaction.objects.filter(user=user, transaction_date__range=(start_date, end_date))
        if account_id:
            tx_qs = tx_qs.filter(account_id=account_id)

        # Расчет суммы доходов и расходов в точном типе Decimal
        total_income = Decimal(tx_qs.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0)
        total_expense = Decimal(tx_qs.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0)
        net_savings = total_income - total_expense

        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'total_balance': float(total_balance),
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'net_savings': float(net_savings),
            'currency': 'UZS'
        })

# Класс отчета со структурой и процентами по категориям
class CategoryBreakdownReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Kategoriya kesimidagi hisobot va foizlar",
        parameters=[
            OpenApiParameter(name='type', description='EXPENSE yoki INCOME', required=False, type=str),
            OpenApiParameter(name='period', description='Davr: day, week, month, year, period', required=False, type=str),
            OpenApiParameter(name='start_date', description='Boshlanish sanasi (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='end_date', description='Tugash sanasi (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='lang', description='Til: uz, ru, en', required=False, type=str),
        ],
        tags=["Hisobotlar"]
    )
    # Метод обработки GET запроса отчета по категориям
    def get(self, request):
        user = request.user
        tx_type = request.query_params.get('type', 'EXPENSE')
        period = request.query_params.get('period', 'month')
        start_date, end_date = get_date_range(
            period, 
            request.query_params.get('start_date'), 
            request.query_params.get('end_date')
        )
        lang = request.query_params.get('lang') or request.META.get('HTTP_ACCEPT_LANGUAGE', 'uz')
        lang = lang[:2].lower()

        tx_qs = Transaction.objects.filter(
            user=user, 
            type=tx_type, 
            transaction_date__range=(start_date, end_date)
        )

        account_id = request.query_params.get('account_id')
        if account_id:
            tx_qs = tx_qs.filter(account_id=account_id)

        # Расчет общей суммы транзакций выбранного типа
        grand_total = Decimal(tx_qs.aggregate(total=Sum('amount'))['total'] or 0)

        # Группировка транзакций по категориям и подсчет суммы
        category_sums = tx_qs.values('category').annotate(total=Sum('amount')).order_by('-total')

        categories_data = []
        for item in category_sums:
            cat_id = item['category']
            total = float(item['total'])
            # Расчет процентной доли каждой категории от общей суммы
            percentage = round((total / float(grand_total)) * 100, 1) if grand_total > 0 else 0

            cat_obj = Category.objects.filter(id=cat_id).first() if cat_id else None
            categories_data.append({
                'category_id': cat_id,
                'category_name': cat_obj.get_name(lang) if cat_obj else ("Boshqa" if lang=='uz' else "Другие" if lang=='ru' else "Other"),
                'icon': cat_obj.icon if cat_obj else 'grid',
                'color': cat_obj.color if cat_obj else '#9E9E9E',
                'total_amount': total,
                'percentage': percentage
            })

        return Response({
            'type': tx_type,
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'grand_total': float(grand_total),
            'categories': categories_data
        })
