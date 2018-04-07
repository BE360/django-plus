from django_plus.fa import fa_convert
from ._generator_ import admin_field_generator
from .utils import str_periodic_inserter


def currency(verbose_name="", path_to_field=None, wrap_white_space=True,
             postfix='تومان', split_length=3, splitter=','):

    def function_changer(func, admin, instance):

        amount = func(admin, instance)

        if amount:
            result = fa_convert(str(amount))

            if result and splitter and split_length > 0:
                result = str_periodic_inserter(result, split_length, splitter)

        else:
            result = ""

        if len(postfix) > 0:
            result += ' ' + postfix

        return result

    return admin_field_generator(
        verbose_name=verbose_name,
        path_to_field=path_to_field,
        function_changer=function_changer,
        wrap_white_space=wrap_white_space
    )

