import datetime

import jdatetime
from django import template

from django_plus.fa import fa_convert, fa_currency

register = template.Library()


@register.filter(name='fa_date')
def fa_date_filter(value, date_format='%Y/%m/%d'):

    if isinstance(value, datetime.date):
        value = jdatetime.date.fromgregorian(date=value)

    if not isinstance(value, jdatetime.date):
        raise Exception("Value type is not valid.")

    return fa_convert(value.strftime(date_format))


@register.filter(name='fa_datetime')
def fa_datetime_filter(value, date_format='%Y/%m/%d ساعت %H:%M:%S'):

    if isinstance(value, datetime.datetime):
        value = jdatetime.datetime.fromgregorian(datetime=value)

    if not isinstance(value, jdatetime.datetime):
        raise Exception("Value type is not valid.")

    return fa_convert(value.strftime(date_format))


@register.filter(name='fa_currency')
def fa_currency_filter(value):

    if isinstance(value, int):
        return fa_currency(value)

    else:
        return value
