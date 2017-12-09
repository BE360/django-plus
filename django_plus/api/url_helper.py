from typing import List
from django_plus.api import cleanifier as cleaners
import collections


class UrlParam:

    int = cleaners.clean_integer
    int_pos = cleaners.clean_pos_integer
    int_pos0 = cleaners.clean_pos_integer0
    clamp_int = cleaners.clamp_int
    int_int_pair_list = cleaners.clean_pair_list_generator(int, int)

    bool = cleaners.clean_bool

    string = cleaners.clean_string
    advanced_string = cleaners.advanced_string_cleaner
    exists_in_array = cleaners.clean_exists_in_array

    datetime = cleaners.clean_datetime

    hash_list = cleaners.clean_by_hash_table_list
    hash = cleaners.clean_by_hash_table

    dictionary = cleaners.clean_dict
    json = cleaners.clean_json

    ignore = lambda x: None

    def __init__(self, key, data_type: str, stored_key: str=None, required: bool=False, default=None, meta=None):
        self.key = key
        self.data_type = data_type
        self.required = required
        self.default = default
        self.meta = meta

        if stored_key is None:
            self.stored_key = key
        else:
            self.stored_key = stored_key

    @staticmethod
    def clean_data(data: dict, params: List['UrlParam']):
        valid_data = {}

        if params is None:
            return valid_data

        if data is None or not isinstance(params, collections.Iterable):
            return None

        # check if keys are not none and corresponding data appear in data dictionary
        for param in params:
            if param is None:
                return None

            try:
                stored_key = param.stored_key
                data_type = param.data_type
                required = param.required

                value = data.get(stored_key, None)

                if value is None:

                    if param.default is not None:
                        value = param.default

                    elif required:
                        return None

                else:
                    value = UrlParam.__clean(value=value, data_type=data_type)

                    if value is None:

                        if param.default is not None:
                            value = param.default

                        elif required:
                            return None

                valid_data[param.key] = value

            except:
                return None

        return valid_data

    @staticmethod
    def __clean(value, data_type):

        return data_type(value)
