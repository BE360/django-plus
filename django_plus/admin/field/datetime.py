from django_plus.admin.field import date
from django_plus.persian_date import CUSTOM_DATETIME_FORMAT


def datetime(verbose_name="", path_to_field=None, time_format=CUSTOM_DATETIME_FORMAT):
    return date(verbose_name, path_to_field, time_format)
