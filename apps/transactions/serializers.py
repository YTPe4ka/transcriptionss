from rest_framework import serializers
from .models import Transaction
from apps.accounts.models import Account
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer
from apps.accounts.serializers import AccountSerializer

class TransactionSerializer(serializers.ModelSerializer):
    account_detail = AccountSerializer(source='account', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)

    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Transaction
        fields = (
            'id', 'type', 'amount', 'account', 'account_detail', 
            'category', 'category_detail', 'transaction_date', 
            'comment', 'photo', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_account(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("Ushbu hisob sizga tegishli emas.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
