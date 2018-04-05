from django_plus.fa import fa_convert
from ._generator_ import admin_field_generator


def currency(verbose_name="", path_to_field=None, postfix='تومان', wrap_white_space=True):

    def function_changer(func, admin, instance):

        amount = func(admin, instance)

        if amount:
            result = fa_convert(str(amount))
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

