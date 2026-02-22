import django_filters
from .models import Item

class ItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="item_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="item_price", lookup_expr='lte')
    item_name = django_filters.CharFilter(field_name="item_name", lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ['is_available']