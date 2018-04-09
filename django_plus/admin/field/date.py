from django_plus.fa.templatetags.fa_tags import fa_date_filter
from ._generator_ import admin_field_generator


def date(verbose_name="", path_to_field=None, time_format='%Y/%m/%d',
         wrap_white_space=True):

    def function_changer(func, admin, instance):

        result_date = func(admin, instance)
        if result_date:
            return fa_date_filter(result_date, time_format)
        else:
            return ""

    return admin_field_generator(
        verbose_name=verbose_name,
        path_to_field=path_to_field,
        function_changer=function_changer,
        wrap_white_space=wrap_white_space
    )
