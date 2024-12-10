from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from . import views


urlpatterns = [
    path('expense_summary/', views.ExpenseSummaryView.as_view(), name='expense_summary'),

]


router = SimpleRouter()
router.register(prefix='expense', viewset=views.ExpenseViewSet, basename='expense')

urlpatterns += router.urls