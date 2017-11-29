from dateutil import parser as dateutil_parser
import os
import json


def clean_string(string):
    try:
        return str(string)
    except:
        return None


def advanced_string_cleaner(min_length: int=None, max_length: int=None, startswith: str=None,
                            endswith: str=None, ):

    def clean(val):
        val = clean_string(val)

        if val is None:
            return None

        if min_length and len(val) < min_length:
            return None

        if max_length and len(val) > max_length:
            return None

        if startswith and not val.startswith(startswith):
            return None

        if endswith and not val.endswith(endswith):
            return None

        return val

    return clean


def clean_integer(num):
    try:
        return int(num)
    except:
        return None


def clean_pos_integer(num):
    cleaned = clean_integer(num)

    if cleaned is None or cleaned <= 0:
        return None

    return cleaned


def clean_pos_integer0(num):
    cleaned = clean_integer(num)

    if cleaned is None or cleaned < 0:
        return None

    return cleaned


def clean_range_int(min_val, max_val):

    def clean(num):
        cleaned = clean_integer(num)

        if cleaned is None or cleaned < min_val or cleaned > max_val:
            return None

        return cleaned

    return clean


def clamp_int(min_val, max_val):

    def clean(num):
        cleaned = clean_integer(num)

        if cleaned is None:
            return None

        if cleaned < min_val:
            cleaned = min_val

        elif cleaned > max_val:
            cleaned = max_val

        return cleaned

    return clean


def clean_bool(val):

    if val in ['0', 'false', 'False', 'None', 'null', 'Null']:
        return False

    try:
        return bool(val)
    except:
        return None


def clean_by_hash_table(hash_table: dict):

    reversed_hash_table = {v: k for k, v in hash_table.items()}

    def clean(val):
        try:
            return reversed_hash_table[val]
        except KeyError:
            return None

    return clean


def clean_by_hash_table_list(hash_table: dict, splitter='|', ignore_invalid_elements=True):

    def clean(val):

        val = clean_string(val)

        if val is None or len(val) == 0:
            return None

        parts = val.split(splitter)
        cleaned_list = []

        cleaner = clean_by_hash_table(hash_table)

        for part in parts:
            cleaned = cleaner(part)

            if cleaned is None:
                if ignore_invalid_elements:
                    continue
                else:
                    return None
            else:
                cleaned_list.append(cleaned)

        return cleaned_list

    return clean


def clean_datetime(date_str):
    try:
        date = dateutil_parser.parse(date_str)

        if date is None:
            return None

        return date
    except:
        return None


def clean_domain(url):
    """
    Clean Domain only for example: http://www.google.com/something will turn to google.com
    :param url:
    :return:
    """
    try:
        url = url.replace("http://", "")
        url = url.replace("https://", "")
        if url.startswith("www."):
            url = url[4:]

        url_arr = url.split("/")
        url = url_arr[0]
        return url
    except:
        return None


def clean_url_protocol_and_www(url):
    """
    Clean Domain only for example: http://www.google.com/something will turn to google.com/something
    :param url:
    :return:
    """
    try:
        url = url.replace("http://", "")
        url = url.replace("https://", "")
        if url.startswith("www."):
            url = url[4:]
        return url
    except:
        return None


def clean_pair_list_generator(first_cleaner=None, second_cleaner=None, list_separator='-', pair_separator=':'):

    def clean(val):
        val = clean_string(val)

        if val is None or len(val) == 0:
            return None

        result = []
        pairs = val.split(list_separator)

        for pair in pairs:
            pair_parts = pair.split(pair_separator)

            if len(pair_parts) >= 2:

                first = pair_parts[0]

                if first_cleaner is not None:
                    first = first_cleaner(first)

                second = pair_parts[1]

                if second_cleaner is not None:
                    second = second_cleaner(second)

                if first is not None and second is not None:
                    result.append((first, second))

        return result

    return clean


def clean_exists_in_array(values_list: list):

    def clean(val):

        if val in values_list:
            return val
        else:
            return None

    return clean


def clean_dict(params: list):

    from django_plus.api import UrlParam

    def clean(data: dict):

        return UrlParam.clean_data(data, params)

    return clean


def clean_json(params: list):

    from django_plus.api import UrlParam

    def clean(data_str: str):

        try:
            data_str = data_str.replace('\'', '\"')
            data = json.loads(data_str)

        except:
            return None

        return UrlParam.clean_data(data, params)

    return clean
