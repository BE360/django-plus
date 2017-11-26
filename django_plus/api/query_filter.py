from typing import List
from django_plus.api import QueryParam


class QueryFilter:
    eq = 'eq'
    gte = 'gte'
    lte = 'lte'

    orderby = 'orderby'

    def __init__(self, field, comparison=eq, ):
        self.field_name = field
        self.comparison_type = comparison

    def get_filter_key(self):
        key = self.field_name

        if self.comparison_type == self.gte:
            key += '__gte'

        elif self.comparison_type == self.lte:
            key += '__lte'

        return key


def filter_by_queries(params_layout: List[QueryParam], param_data, queryset):

    filter_dict = {}

    # Choosing valid queries
    for param in params_layout:

        param_filter = param.meta

        if isinstance(param_filter, QueryFilter):
            filter_key = param_filter.get_filter_key()
            filter_value = param_data[param.key]

            if filter_value:
                filter_dict[filter_key] = filter_value

    try:
        queryset = queryset.filter(**filter_dict)
    except:
        pass

    queryset = check_for_order_by(param_data, queryset)

    return queryset


def check_for_order_by(filter_data, queryset):

    order_by_field = filter_data.get(QueryFilter.orderby, None)

    if order_by_field:

        if order_by_field is not None:
            try:
                queryset = queryset.order_by(order_by_field)
            except:
                pass

    return queryset
