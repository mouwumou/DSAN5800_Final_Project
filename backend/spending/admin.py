from django.contrib import admin
from .models import ExpenseCategory, Merchant, Expense

# Register your models here.
@admin.register(ExpenseCategory)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Merchant)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Expense)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'expense_date', 'user', 'merchant', 'category', 'description', 'created_at', 'updated_at')