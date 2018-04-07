from django_plus.fa import fa_convert
from ._generator_ import admin_field_generator
from .utils import str_periodic_inserter


def number(verbose_name="", path_to_field=None, wrap_white_space=True, split_length=3,
           splitter=','):

    def function_changer(func, admin, instance):

        amount = func(admin, instance)

        if amount:
            num = fa_convert(str(amount))
        else:
            num = ""

        if num and split_length > 0 and splitter:
            num = str_periodic_inserter(num, split_length, splitter)

        return num

    return admin_field_generator(
        verbose_name=verbose_name,
        path_to_field=path_to_field,
        function_changer=function_changer,
        wrap_white_space=wrap_white_space
    )

