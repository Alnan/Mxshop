from django.db.models import Q
import django_filters
from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    自定义过滤器，实现区间过滤
    商品过滤的类
    '''
    #filters.NumberFilter有两个参数，name是要过滤的字段，lookup是执行的行为，‘小与等于本店价格’
    pricemin = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lte')

    # 行为: 名称中包含某字符，且字符不区分大小写
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    # 方法：自定义过滤条件 ，field_name：字段名 ， method：指定自定义方法
    top_category = django_filters.NumberFilter(field_name="category", method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        # 不管当前点击的是一级目录二级目录还是三级目录,返回过滤后的数据
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax','top_category','is_hot','is_new']