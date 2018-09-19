# from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

from goods.serializers import GoodsSerializer,CategorySerializer,BannerSerializer,IndexCategorySerializer
from .models import Goods,GoodsCategory,Banner
from goods.filter import GoodsFilter

# class GoodsListView(APIView):
#     '''
#     商品列表
#     '''
#     def get(self,request,format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serialzer = GoodsSerializer(goods,many=True)
#         return Response(goods_serialzer.data)
#
#         # post方法，客户端输入数据提交时触发
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)  # 将用户输入数据传入到GoodsSerializers中，类似django中form的post方法
#         if serializer.is_valid():  # 判断数据是否一致，没错误
#             serializer.save()  # 保存
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GoodsListView(generics.ListAPIView):
#     # setting中做好分页配置，即可实现分页效果，  ListAPIView内置分页功能
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer

# 分页自定义化设置，此时可以注销setting.py中的REST_FRAMEWORK
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'  #每页10个数据
    page_query_param = 'page'   #url过滤信息，‘page=**’
    max_page_size = 100   #最大100个数据

# class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
#     '商品列表页'
#
#     # 分页
#     pagination_class = GoodsPagination
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer

class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
        商品列表页数据
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    queryset = Goods.objects.all()
    # 分页
    pagination_class = GoodsPagination
    # 序列化
    serializer_class = GoodsSerializer
    # 过滤、搜索、排序
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    # 设置filter过滤字段
    # filter_fields = ('name','shop_price')

    # 设置filter的类为我们自定义的类  过滤
    filter_class = GoodsFilter

    # 设置我们的search字段  搜索
    search_fields = ('name', 'goods_brief', 'goods_desc')

    # 设置排序
    ordering_fields = ('sold_num', 'shop_price')

    # 商品点击数 + 1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取is_tab=True（导航栏）里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料","奶类食品"])
    serializer_class = IndexCategorySerializer