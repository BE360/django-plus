import re
from django.utils import formats
import jdatetime


def jalali(time, time_format=None):

    if time_format is None:
        return jdatetime.datetime.fromgregorian(datetime=time)
    else:
        try:
            time_jalali = jdatetime.datetime.fromgregorian(datetime=time)
        except:
            time_jalali = jdatetime.datetime.fromgregorian(date=time)
        time_string = formats.date_format(time_jalali, time_format)
        time_string = time_string.replace("ژانویه", "فروردین")
        time_string = time_string.replace("فوریه", "اردیبهشت")
        time_string = time_string.replace("مارس", "خرداد")
        time_string = time_string.replace("آوریل", "تیر")
        time_string = time_string.replace("مه", "مرداد")
        time_string = time_string.replace("ژوئن", "شهریور")
        time_string = time_string.replace("ژوئیه", "مهر")
        time_string = time_string.replace("اوت", "آبان")
        time_string = time_string.replace("سپتامبر", "آذر")
        time_string = time_string.replace("اکتبر", "دی")
        time_string = time_string.replace("نوامبر", "بهمن")
        time_string = time_string.replace("دسامبر", "اسفند")

        weekdays_map = {
            "شنبه": "پنج‌شنبه",
            "یک‌شنبه": "جمعه",
            "یکشنبه": "جمعه",
            "یک ‌شنبه": "جمعه",
            "دوشنبه": "شنبه",
            "دو‌شنبه": "شنبه",
            "سه‌شنبه": "یک‌شنبه",
            "سه شنبه": "یک‌ شنبه",
            "چهارشنبه": "دوشنبه",
            "چهار‌شنبه": "دو‌شنبه",
            "پنجشنبه": "سه‌شنبه",
            "پنج‌شنبه": "سه‌شنبه",
            "جمعه": "چهارشنبه"
        }

        pattern = re.compile(r'\b(' + '|'.join(weekdays_map.keys()) + r')\b')
        time_string = pattern.sub(lambda x: weekdays_map[x.group()], time_string)

        return time_string
