from datetime import timedelta


def fa_convert(latin_str: str):
    try:
        latin_str = latin_str.replace('0', u'۰')
        latin_str = latin_str.replace('1', u'۱')
        latin_str = latin_str.replace('2', u'۲')
        latin_str = latin_str.replace('3', u'۳')
        latin_str = latin_str.replace('4', u'۴')
        latin_str = latin_str.replace('5', u'۵')
        latin_str = latin_str.replace('6', u'۶')
        latin_str = latin_str.replace('7', u'۷')
        latin_str = latin_str.replace('8', u'۸')
        latin_str = latin_str.replace('9', u'۹')
        latin_str = latin_str.replace(',', '،')
        return latin_str
    except:
        return latin_str


def fa_timedelta(_timedelta: timedelta):
    to_persian = str(_timedelta).replace("days", "روز").replace("day", "روز").split('.')[0]

    return fa_convert(to_persian)


def fa_number(amount, number_split=3, splitter=','):
    amount_str = fa_convert(str(amount))

    if number_split > 0:
        amount_str = str_periodic_inserter(amount_str, number_split, splitter)

    return amount_str


def fa_currency(amount, number_split=3, splitter=',', postfix="تومان"):

    return fa_number(amount, number_split, splitter) + " " + postfix


def str_periodic_inserter(target_str, parts_length, splitter, start_from_right=True):

    if start_from_right:
        target_str = target_str[::-1]

    result = splitter.join(
        target_str[i:i + parts_length] for i in range(0, len(target_str), parts_length)
    )

    if start_from_right:
        result = result[::-1]

    return result
