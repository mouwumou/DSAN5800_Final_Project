from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Merchant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.FloatField()
    expense_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<User: %s Expense: %s on %s>' % (self.user.username, self.amount, self.expense_date)
