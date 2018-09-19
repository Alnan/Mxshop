from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from .serializers import SmsSerializer,UserRegSerializer,UserDetailSerializer
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework import viewsets
from rest_framework import status
from utils.yunpian import YunPian
from Mxshop.settings import APIKEY
from random import choice
from .models import VerifyCode
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions

User = get_user_model() # 当前用户

class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能直接password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password)方法，及加密后的密码
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    '''
    用户注册，发送手机验证码
    '''
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        #验证合法
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)
        #生成验证码
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save() # 保存验证码及手机号
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,viewsets.GenericViewSet):
    """
    create:
        用户注册
    retrieve:
        获取用户信息
    update:
        更新用户信息
    partial_update:
        更新用户信息（部分更新）
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication) # 用户认证

    def get_permissions(self): # 权限
        if self.action == "retrieve":  # 获取用户信息
            return [permissions.IsAuthenticated()]
        elif self.action == "create":  # 新用户注册
            return []
        return []

    def get_serializer_class(self): # 用户信息序列化
        if self.action == "retrieve":  # 获取用户信息
            return UserDetailSerializer
        elif self.action == "create":  # 新用户注册
            return UserRegSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):  # 重载create方法
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)  # 设置token
        re_dict["name"] = user.name if user.name else user.username  # 设置用户名

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 获取当前用户，
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()