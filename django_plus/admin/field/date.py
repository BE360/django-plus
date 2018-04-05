from django_plus.fa import jalali, CUSTOM_DATE_FORMAT
from ._generator_ import admin_field_generator


def date(verbose_name="", path_to_field=None, time_format=CUSTOM_DATE_FORMAT,
         wrap_white_space=True):

    def function_changer(func, admin, instance):

        result_date = func(admin, instance)
        if result_date:
            return jalali(result_date, time_format)
        else:
            return ""

    return admin_field_generator(
        verbose_name=verbose_name,
        path_to_field=path_to_field,
        function_changer=function_changer,
        wrap_white_space=wrap_white_space
    )

