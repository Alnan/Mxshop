from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user_operation.models import UserFav,UserLeavingMessage,UserAddress
from goods.serializers import GoodsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情
    要展示商品详情，则需结合商品序列化，重新创建user收藏类序列化
    '''
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ("goods", "id")

class UserFavSerializer(serializers.ModelSerializer):
    """用户新增收藏"""
    # 获取当前登录的用户，并隐藏不展示到api接口中
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        #UniqueTogetherValidator用于唯一联合验证，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                #message自定义错误消息
                message="已经收藏"
            )
        ]
        model = UserFav
        #返回商品的id(goods是外键，在UserFav表中显示就是商品id：goods_id），用于取消收藏时delete操作调用
        fields = ("user", "goods",'id')

class LeavingMessageSerializer(serializers.ModelSerializer):
    '''
    用户留言
    '''
    # 获取当前登录的用户， 隐藏不显示到api接口
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    #read_only:只返回，post时候可以不用提交，format：格式化输出
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id" ,"add_time")


class AddressSerializer(serializers.ModelSerializer):
    """收货地址"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")