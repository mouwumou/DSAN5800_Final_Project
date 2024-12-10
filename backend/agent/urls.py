from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from . import views


urlpatterns = [
    path('agent/', views.AgentView.as_view(), name='agent'),
    path('history/<str:session_id>/', views.SessionHistoryView.as_view(), name='session-history'),

]


router = SimpleRouter()
router.register(prefix='tool', viewset=views.ToolViewSet, basename='tool')

urlpatterns += router.urls