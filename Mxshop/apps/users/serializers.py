import re
from datetime import datetime, timedelta
from Mxshop.settings import REGEX_MOBILE
from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    # 函数名必须：validate + 验证字段名
    def validate_mobile(self, mobile):
        """
        手机号码验证
        """
        # 是否已经注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        # 60s内只能发送一次
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """用户注册"""
    #model中user表没有code字段，此字段是新增，用来验证前端用户注册输入的验证码
    code = serializers.CharField(label="验证码",required=True, write_only=True, max_length=4, min_length=4, error_messages={
        "blank": "请输入验证码",
        "required": "请输入验证码",
        "max_length": "验证码格式错误",
        "min_length": "验证码格式错误"
    },
         help_text="验证码")
    #用户名验证,如果存在则报错
    username = serializers.CharField(label="用户名", help_text="用户名(必须手机号）", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="手机号已经存在")])
    #后端验证成功会把数据序列化显示到api接口中，设置write_only=True，让序列化时忽略此字段
    password = serializers.CharField(label="密码",style={'input_type':'password'},write_only=True)

    def validate_code(self, code):# 验证码验证
        # 验证码在数据库中是否存在，用户从前端post过来的值都会放入initial_data里面，排序(最新一条)。
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            # 获取到最新一条
            last_record = verify_records[0]

            # 有效期为五分钟。
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self,attrs):#每个字段验证成功后，都会添加到attrs这个字段中，attrs是个字典类型
        #用户注册用手机号，但前端属性注明是username，故需要将username中的值传给mobile
        print(attrs)
        attrs["mobile"] = attrs["username"]
        del attrs["code"] #User没有code这个字段，用完可以del掉
        return attrs

    #验证成功后，需要保存密码，后端调用.save()时，触发此处create方法，密码没进行验证，只加密处理
    def create(self, validated_data):# 重载父类create方法
        user =super(UserRegSerializer,self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["username","code","password","mobile"]

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email","mobile")