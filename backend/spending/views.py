from django.shortcuts import render
from django.db.models import Sum

from rest_framework import status, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Expense, ExpenseCategory
from .serializers import CategorySerializer, ExpenseSerializer


# Create your views here.
class ExpenseSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user)
        summary = expenses.values('category__name').annotate(total_spending=Sum('amount'))
        return Response(summary)
    
class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user-specific expenses.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter expenses by the authenticated user.
        """
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user to the expense.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def filter_by_category(self, request):
        """
        Custom action to filter expenses by category.
        """
        category = request.query_params.get('category', None)
        if category:
            expenses = self.get_queryset().filter(category=category)
            serializer = self.get_serializer(expenses, many=True)
            return Response(serializer.data)
        return Response({"detail": "Category parameter is required."}, status=400)

    @action(detail=False, methods=['get'])
    def filter_by_date_range(self, request):
        """
        Custom action to filter expenses by date range.
        """
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date and end_date:
            expenses = self.get_queryset().filter(expense_date__range=[start_date, end_date])
            serializer = self.get_serializer(expenses, many=True)
            return Response(serializer.data)
        return Response({"detail": "Start and end dates are required."}, status=400)

class CategoryView(APIView):
    def get(self, request):
        categories = ExpenseCategory.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = CategorySerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
