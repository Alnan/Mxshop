# encoding: utf-8

# 独立使用django的model
import sys
import os
#  获取当前文件的路径，即Mxshop/db_tools
pwd = os.path.dirname(os.path.realpath(__file__))
# 往上一级，回到根目录，即/Mxshop
sys.path.append(pwd + "../")
# django环境，需先设置，才能使用django相关
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VueDjangoFrameWorkShop.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mxshop.settings")

import django
# 初始化django
django.setup()

# 这行代码必须在初始化django之后
from goods.models import GoodsCategory

from db_tools.data.category_data import row_data

# 一级分类
for lev1_cat in row_data:
    lev1_intance = GoodsCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()

    # 该一级分类之下的二级分类
    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = GoodsCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        # 该二级分类之下的三级分类
        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodsCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()

