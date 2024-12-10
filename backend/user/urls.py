from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path('token/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test_auth', views.test_auth, name='test_auth'),
    ]

# urlpatterns = format_suffix_patterns(urlpatterns)

router = SimpleRouter()  # 实例化一个简单路由
router.register(prefix='user', viewset=views.UserView, basename='user') # 注册路由
router.register(prefix='user_manage', viewset=views.UserViewSet, basename="user_manage")
urlpatterns += router.urls  # 合并到urlpatterns列表里