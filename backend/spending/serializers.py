from rest_framework import serializers

from .models import Expense, ExpenseCategory

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'amount', 'expense_date', 'merchant', 'category', 'description', 'created_at', 'updated_at')
        read_only_fields = ['user', 'created_at']

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ('id', 'name')