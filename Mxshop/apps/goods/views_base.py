# encoding: utf-8
from goods.models import Goods

from django.views.generic.base import View

# 用于测试
class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        """
        json_list = []
        goods = Goods.objects.all()[:10]

        # for good in goods:
        #     json_dict = {}
        #     json_dict["name"] = good.name
        #     json_dict["category"] = good.category.name
        #     json_dict["market_price"] = good.market_price
        #     json_dict["add_time"] = good.add_time
        #     json_list.append(json_dict)
        #
        # from django.http import HttpResponse
        # return HttpResponse(json_list,content_type="application/json")


        # from django.forms.models import model_to_dict  # 将model中数据转成字典格式
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        import json
        from django.core import serializers
        from django.http import HttpResponse, JsonResponse
        json_data = serializers.serialize('json', goods) # 按json格式，直接序列化goods ，任何格式都能序列化
        json_data = json.loads(json_data) # 反序列化

        return HttpResponse(json_data, content_type="application/json")
        # jsonResponse做的工作也就是加上了dumps和content_type
        # return JsonResponse(json_data, safe=False)



