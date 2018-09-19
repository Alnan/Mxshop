"""Mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path,include,re_path
import xadmin
from django.views.static import serve  # 用于寻找静态文件
from Mxshop.settings import MEDIA_ROOT
# from goods.views import GoodsListView
from rest_framework.documentation import include_docs_urls  # drf
from rest_framework.routers import DefaultRouter  # 导入DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework.authtoken import views  #drf 自带token验证
from django.views.generic import TemplateView

from goods.views import GoodsListViewSet,CategoryViewset,BannerViewset,IndexCategoryViewset
from users.views import SmsCodeViewset,UserViewset
from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewset
from trade.views import ShoppingCartViewset,OrderViewset


router = DefaultRouter()  #实例化router
router.register(r'goods', GoodsListViewSet,base_name="goods") # 配置GoodsCategory的url

# 配置商品分类的url
router.register(r'categorys', CategoryViewset, base_name="categorys")
# 配置验证码的url
router.register(r'code', SmsCodeViewset, base_name="code")
# 用户注册
router.register(r'users', UserViewset, base_name="users")
# 用户收藏
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
# 用户留言
router.register(r'messages', LeavingMessageViewset, base_name="messages")
# 收货地址
router.register(r'address',AddressViewset , base_name="address")
# 购物车
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")
# 订单的url
router.register(r'orders', OrderViewset, base_name="orders")
# 首页轮播图的url
router.register(r'banners', BannerViewset, base_name="banners")
# 首页系列商品展示url
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    # 这句代码意思是，与media相关的通通当作静态文件来处理，根据指定好的MEDIA_ROOT路径找寻静态文件
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),

    # path('api-token-auth/', views.obtain_auth_token),  # drf自带的token用户验证模式
    re_path('login/$', obtain_jwt_token ), # jwt的用户认证模式 ，用户登录

    # 首页
    path('index/', TemplateView.as_view(template_name='index.html'),name='index'),

    # 商品列表页
    # path('goods/', GoodsListView.as_view(),name="goods_list"),
    # router的path路径
    re_path('^', include(router.urls)),

    # 自动化文档,1.11版本中注意此处前往不要加$符号
    path('docs/', include_docs_urls(title='生鲜电商')),
    # 调试登录，可用admin账号登录drf页面
    path('api-auth/', include('rest_framework.urls')),
    # 第三方登录
    path('', include('social_django.urls', namespace='social'))
]
