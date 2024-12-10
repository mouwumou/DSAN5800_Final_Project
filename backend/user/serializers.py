from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

from .models import Profile

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('name', 'phone')
        read_only_fields = ('name', 'phone')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ("username", "profile", "is_superuser")
        read_only_fields = ("__all__",)


class RegSerializers(serializers.ModelSerializer):
    pwd2=serializers.CharField(max_length=256, min_length=4, write_only=True)
    # tel=serializers.CharField(max_length=11,min_length=11)

    class Meta:
        model = User
        fields=('username','password','pwd2')

    def validate(self, attrs):
        if attrs['pwd2'] != attrs['password']:
            raise serializers.ValidationError('两次密码输入不一致')
        del attrs['pwd2']
        # 对密码进行加密 make_password
        attrs['password'] = make_password(attrs['password'])
        return attrs
