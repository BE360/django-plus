from django_plus.admin.field import date


def datetime(verbose_name="", path_to_field=None, time_format="%Y/%m/%d ساعت %H:%i:%s",
             wrap_white_space=True):
    return date(verbose_name, path_to_field, time_format, wrap_white_space)
