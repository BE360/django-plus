

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