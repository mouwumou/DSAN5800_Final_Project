from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限只允许对象的创建者才能编辑它。"""
    def has_object_permission(self, request, view, obj):
        # 读取权限被允许用于任何请求，
        # 所以我们始终允许 GET，HEAD 或 OPTIONS 请求。
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写入权限只允许给 article 的作者。
        return obj.author == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    只有管理员拥有编辑权限，其他人拥有查看权限"""
    def has_permission(self, request, view):
        # 可读权限
        if request.method == "GET":
            return True
        # 写入权限只允许给 article 的作者。
        return request.user.is_superuser

class IsUserOwn(permissions.BasePermission):
    """
    只有用户自己能查看"""
    def has_permission(self, request, view):
        print(request.auth)
        print(type(request.user))
        if request.method == "GET":
            return True
        return request.user.is_superuser