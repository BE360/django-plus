
class QueryFilter:
    eq = 'eq'
    gte = 'gte'
    lte = 'lte'

    def __init__(self, field, stored_key=None, comparison=eq, cleaner=None):

        if stored_key is None:
            stored_key = field

        self.stored_key = stored_key
        self.field_name = field
        self.comparison_type = comparison

        self.cleaner_func = cleaner

    def __bake__(self, data):
        value = data.get(self.stored_key)

        if value is None:
            return None

        if self.cleaner_func is not None:
            value = self.cleaner_func(value)

        if value is None:
            return None

        key = self.field_name

        if self.comparison_type == self.gte:
            key += '__gte'

        elif self.comparison_type == self.lte:
            key += '__lte'

        return key, value


class QueryFilterBaker:

    orderby = 'orderby'

    def __init__(self, query_model_list, order_by_cleaner=None, enable_ordering=True):
        self.query_model_list = query_model_list
        self.order_by_cleaner = order_by_cleaner
        self.enable_ordering = enable_ordering

    def check_for_order_by(self, data, queryset):

        order_by_field = data.get(self.orderby, None)

        if order_by_field is not None:
            if self.order_by_cleaner is not None:
                order_by_field = self.order_by_cleaner(order_by_field)

            if order_by_field is not None:
                try:
                    queryset = queryset.order_by(order_by_field)
                except:
                    pass

        return queryset

    def bake(self, data, queryset):

        filter_dict = {}

        # Choosing valid queries
        for query in self.query_model_list:

            baked = query.__bake__(data)

            if baked is not None:
                filter_dict[baked[0]] = baked[1]

        try:
            queryset = queryset.filter(**filter_dict)
        except:
            pass

        if self.enable_ordering:
            queryset = self.check_for_order_by(data, queryset)

        return queryset
