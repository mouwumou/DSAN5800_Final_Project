from spending.models import Expense

def write_expense(user, amount, category, merchant, description):
    """
    Write an expense to the database.
    """
    try:
        expense = Expense.objects.create(
            user=user,
            amount=amount,
            category=category,
            merchant=merchant,
            description=description
        )
        expense.save()
        return expense
    except Exception as e:
        return None