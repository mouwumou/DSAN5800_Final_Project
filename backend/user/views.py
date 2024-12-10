import xlrd
import user
from rest_framework import status, viewsets, permissions, generics
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


from .serializers import MyTokenObtainPairSerializer, UserSerializer, ProfileSerializer, RegSerializers
from .models import Profile
from .permissions import IsAdminOrReadOnly
from .pagination import UserPagination

User = get_user_model()

class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        try:
            user = self.request.user
            return User.objects.get(username=user)
        except:
            return False

    # 用户信息
    @action(methods=['get'], detail=False, url_path='user_detail')
    def user_detail(self, request):
        user = self.get_queryset()
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # 修改密码
    @action(methods=['post'], detail=False, url_path='change_password')
    def change_password(self, request):
        user = self.get_queryset()
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            password = request.data["password"]
            npwd = request.data["npwd"]
            npwd2 = request.data["npwd2"]
        except Exception as e:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

        if password == npwd:
            return Response({"新密码不能与旧密码一样"},status=status.HTTP_406_NOT_ACCEPTABLE)
        if npwd != npwd2:
            return Response({"两次密码输入不一致！"},status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(npwd) > 20 or len(npwd) < 8:
            return Response({"密码长度需要8到20位"},status=status.HTTP_406_NOT_ACCEPTABLE)

        if user.check_password(password):
            # 修改密码为新密码
            user.set_password(npwd)
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg': "密码错误"},status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False).order_by('-pk')
    serializer_class = UserSerializer
    pagination_class = UserPagination
    # permission_classes = [permissions.IsAdminUser]
    
    # 用户创建
    def create(self, request):
        username = request.data.get("username")
        password = request.data.get("password", "")
        name = request.data.get("name")
        id_number = request.data.get("id_number")
        phone = request.data.get("phone")
        if not (username and name and id_number and phone):
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        if password == "":
            password = id_number[-6:]
            
        try:
            user = User()
            user.username = username
            user.password = make_password(password)
            user.save()
        except:
            return Response({'msg': '考生号已存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if name and id_number and phone:
            profile = Profile(user=user, name=name, phone=phone)
            profile.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request):
        username = request.data.get("username")
        if not username:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        password = request.data.get("password", "")
        name = request.data.get("name")
        phone = request.data.get("phone")
        if not (name):
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

        if password != "":
            user.password = make_password(password)
            user.save()
        
        profile = Profile.objects.get(user=user)
        profile.name = name
        profile.phone = phone
        profile.save()

        return Response(status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request):
        delete_id = request.query_params.get('delete_id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_list = delete_id.split(',')
        for i in user_list:
            generics.get_object_or_404(User, username=i).delete()
        return Response({"num": len(user_list)}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def test_auth(request):
    return Response({'user': str(request.user)}, status=status.HTTP_200_OK)
