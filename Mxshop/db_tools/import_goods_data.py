# encoding: utf-8

import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VueDjangoFrameWorkShop.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mxshop.settings")

import django
django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    # 价格（￥55元），空格替换掉￥、元，強制转化成float类型
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", ""))) #市场价格
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", ""))) #本店价格
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""  #简单描述
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""  #图片，拿到的是字符串
    # 取第一张作为封面图
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""
    # 取出倒数第一个也就是最小的类
    category_name = goods_detail["categorys"][-1]
    # 取出当前子类对应的GoodsCategory对象
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        # goods外键关联GoodsCategory，让两者关联上
        goods.category = category[0]
    goods.save()

    # 详情页，商品轮播图
    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()