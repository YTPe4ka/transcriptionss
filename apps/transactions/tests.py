from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import Account
from apps.categories.models import Category
from apps.transactions.models import Transaction

User = get_user_model()

class TransactionLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')
        self.account = Account.objects.create(user=self.user, name='Naqd', balance=100000, currency='UZS')
        self.category_exp = Category.objects.create(name_uz='Tushlik', type='EXPENSE')
        self.category_inc = Category.objects.create(name_uz='Oylik', type='INCOME')

    def test_expense_transaction_decreases_balance(self):
        tx = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_exp,
            amount=25000,
            type='EXPENSE'
        )
        self.account.refresh_from_db()
        self.assertEqual(float(self.account.balance), 75000.0)

    def test_income_transaction_increases_balance(self):
        tx = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_inc,
            amount=50000,
            type='INCOME'
        )
        self.account.refresh_from_db()
        self.assertEqual(float(self.account.balance), 150000.0)

    def test_delete_transaction_reverts_balance(self):
        tx = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_exp,
            amount=30000,
            type='EXPENSE'
        )
        self.account.refresh_from_db()
        self.assertEqual(float(self.account.balance), 70000.0)

        tx.delete()
        self.account.refresh_from_db()
        self.assertEqual(float(self.account.balance), 100000.0)
