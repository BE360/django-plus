from django_plus.admin.field import date
from django_plus.persian_date import CUSTOM_DATETIME_FORMAT


def datetime(verbose_name="", path_to_field=None, time_format=CUSTOM_DATETIME_FORMAT,
             wrap_white_space=True):
    return date(verbose_name, path_to_field, time_format, wrap_white_space)
