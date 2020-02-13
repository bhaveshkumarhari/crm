import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    # Date created is greater than or equal to
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    # Date created is less than or equal to
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    # Note filter with ignoring case sensitivity
    note = CharFilter(field_name="note", lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']