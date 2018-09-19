from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    只读操作/只能操作当前用户相关数据
    """
    def has_object_permission(self, request, view, obj):
        #  GET、 HEAD or OPTIONS请求允许操作，因为都是安全的
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        #确定是当前用户才能进行其他操作
        return obj.user == request.user