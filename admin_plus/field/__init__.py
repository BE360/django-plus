from .generator import admin_field_generator
from persian_date.jalali_date import jalali, DatetimeFormat
from django.template.loader import render_to_string


def general(verbose_name="", html=False, boolean=False, path_to_field=None):

    return admin_field_generator(
        verbose_name=verbose_name,
        html=html,
        boolean=boolean,
        path_to_field=path_to_field
    )


def date(verbose_name="", path_to_field=None, time_format=DatetimeFormat.CUSTOM_DATE):

    def function_changer(func, admin, instance):

        result_date = func(admin, instance)
        if result_date:
            return jalali(result_date, time_format)
        else:
            return ""

    return admin_field_generator(
        verbose_name=verbose_name,
        path_to_field=path_to_field,
        function_changer=function_changer
    )


def datetime(verbose_name="", path_to_field=None, time_format=DatetimeFormat.CUSTOM_DATETIME):
    return date(verbose_name, path_to_field, time_format)


def template(template_name, verbose_name=""):

    def function_changer(func, admin_inst, model_inst):
        """
        :param func: returns a context
        :param admin_inst:
        :param model_inst:
        :return:
        """
        ctx = func(admin_inst, model_inst)
        return render_to_string(template_name, ctx)

    return admin_field_generator(
        verbose_name=verbose_name,
        function_changer=function_changer,
        html=True
    )
