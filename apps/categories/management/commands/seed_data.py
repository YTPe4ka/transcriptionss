from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.categories.models import Category
from apps.accounts.models import Account
from apps.transactions.models import Transaction
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = "Boshlangʻich kategoriyalar va namuna maʼlumotlarni yuklaydi."

    def handle(self, *args, **kwargs):
        self.stdout.write("Boshlang'ich kategoriyalar yaratilmoqda...")

        default_categories = [
            # Chiqim turlari (Expenses)
            {'name_uz': "Yo'lkira", 'name_ru': 'Транспорт', 'name_en': 'Transport', 'type': 'EXPENSE', 'icon': 'bus', 'color': '#1976D2'},
            {'name_uz': 'Tushlik (Kafe)', 'name_ru': 'Кафе', 'name_en': 'Cafe', 'type': 'EXPENSE', 'icon': 'utensils', 'color': '#FBC02D'},
            {'name_uz': 'Salomatlik', 'name_ru': 'Здоровье', 'name_en': 'Health', 'type': 'EXPENSE', 'icon': 'heart-pulse', 'color': '#E53935'},
            {'name_uz': 'Mahsulotlar', 'name_ru': 'Продукты', 'name_en': 'Groceries', 'type': 'EXPENSE', 'icon': 'shopping-basket', 'color': '#00ACC1'},
            {'name_uz': 'Hordiq (Dosug)', 'name_ru': 'Досуг', 'name_en': 'Leisure', 'type': 'EXPENSE', 'icon': 'wallet', 'color': '#4CAF50'},
            {'name_uz': 'Uy-joy', 'name_ru': 'Дом', 'name_en': 'Home', 'type': 'EXPENSE', 'icon': 'home', 'color': '#1E88E5'},
            {'name_uz': "Ta'lim", 'name_ru': 'Образование', 'name_en': 'Education', 'type': 'EXPENSE', 'icon': 'graduation-cap', 'color': '#E91E63'},

            # Kirim turlari (Incomes)
            {'name_uz': 'Oylik maosh', 'name_ru': 'Зарплата', 'name_en': 'Salary', 'type': 'INCOME', 'icon': 'briefcase', 'color': '#1E88E5'},
            {'name_uz': 'Sovgʻa', 'name_ru': 'Подарок', 'name_en': 'Gift', 'type': 'INCOME', 'icon': 'gift', 'color': '#E91E63'},
            {'name_uz': 'Depozit foizlari', 'name_ru': 'Проценты по депозитам', 'name_en': 'Deposit Interest', 'type': 'INCOME', 'icon': 'bank', 'color': '#4CAF50'},
            {'name_uz': 'Boshqa', 'name_ru': 'Другое', 'name_en': 'Other', 'type': 'INCOME', 'icon': 'question-circle', 'color': '#8BC34A'},
            {'name_uz': 'Avans', 'name_ru': 'Аванс', 'name_en': 'Advance', 'type': 'INCOME', 'icon': 'cash', 'color': '#FF9800'},
            {'name_uz': 'Kunlik ish haqi', 'name_ru': 'Дневной заработок', 'name_en': 'Daily Wage', 'type': 'INCOME', 'icon': 'coins', 'color': '#009688'},
        ]

        created_count = 0
        for cat in default_categories:
            obj, created = Category.objects.get_or_create(
                name_uz=cat['name_uz'],
                type=cat['type'],
                user=None,
                defaults={
                    'name_ru': cat['name_ru'],
                    'name_en': cat['name_en'],
                    'icon': cat['icon'],
                    'color': cat['color'],
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"{created_count} ta yangi kategoriya muvaffaqiyatli yaratildi."))

        # Demo user creation
        demo_user, u_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Exam',
                'last_name': 'Student',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if u_created:
            demo_user.set_password('admin123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS("Demo superuser 'admin' (parol: admin123) yaratildi."))

        # Demo Accounts
        acc1, _ = Account.objects.get_or_create(user=demo_user, name='Naqd', defaults={'balance': 43000, 'currency': 'UZS', 'color': '#4CAF50', 'icon': 'money'})
        acc2, _ = Account.objects.get_or_create(user=demo_user, name='UzCard SQB', defaults={'balance': 47000, 'currency': 'UZS', 'color': '#2196F3', 'icon': 'credit-card'})
        acc3, _ = Account.objects.get_or_create(user=demo_user, name='USD', defaults={'balance': 800, 'currency': 'UZS', 'color': '#00BCD4', 'icon': 'dollar'})

        # Sample Transactions matching screenshots: Cafe 25000, Groceries 15000, Transport 5000
        cat_cafe = Category.objects.filter(name_uz='Tushlik (Kafe)').first()
        cat_groceries = Category.objects.filter(name_uz='Mahsulotlar').first()
        cat_transport = Category.objects.filter(name_uz="Yo'lkira").first()

        today = timezone.now().date()
        if cat_cafe:
            Transaction.objects.get_or_create(user=demo_user, account=acc1, category=cat_cafe, amount=25000, type='EXPENSE', transaction_date=today, comment='Tushlik Kafe')
        if cat_groceries:
            Transaction.objects.get_or_create(user=demo_user, account=acc2, category=cat_groceries, amount=15000, type='EXPENSE', transaction_date=today, comment='Bozaar mahsulotlar')
        if cat_transport:
            Transaction.objects.get_or_create(user=demo_user, account=acc1, category=cat_transport, amount=5000, type='EXPENSE', transaction_date=today, comment='Taksi Yo\'lkira')

        self.stdout.write(self.style.SUCCESS("Hisoblar va demo ma'lumotlar tayyor."))

