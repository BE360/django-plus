from datetime import datetime
from collections import Counter

COOKIE_ENCRYPTION_KEY = "azsecrfbvtuhly0p1234567890~:#|- "
COOKIE_DECRYPTION_KEY = "953684217-*%#@~.azsecrfbvtuhly0k"
COOKIE_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
COOKIE_DATE_FORMAT = "%Y-%m-%d"

SPLITTER = '|'
PAIR_SEPARATOR = '~'
TIME_SEPARATOR = '#'
PARTIAL_TIME_SEPARATOR = '$'


def cookie_encrypt(cookie_str: str, encryption=False) -> str:
    """
    encrypt string with translate function
    :param cookie_str: raw input string
    :param encryption: encrypt or not
    :return: encrypted string to usually be saved in cookie's value
    """
    if not encryption:
        return cookie_str
    trans_tab = str.maketrans(COOKIE_ENCRYPTION_KEY, COOKIE_DECRYPTION_KEY)
    return cookie_str.translate(trans_tab)


def cookie_decrypt(encrypted_str: str, encryption=False) -> str:
    """
    decrypt string with translate function
    :param encrypted_str: input usually from cookie's value
    :param encryption: encrypted or not
    :return: decrypted string
    """
    if not encryption:
        return encrypted_str
    trans_tab = str.maketrans(COOKIE_DECRYPTION_KEY, COOKIE_ENCRYPTION_KEY)
    return encrypted_str.translate(trans_tab)


def cookie_str_to_time(value: str) -> datetime:
    """
    time formatted string to datetime
    :param value: time formatted string (Date formatted 2017-07-13 or Timestamp formatted 2017-07-13 10:18:20)
    :return: datetime object
    """
    try:
        return datetime.strptime(value, COOKIE_TIMESTAMP_FORMAT)
    except ValueError:
        return datetime.strptime(value, COOKIE_DATE_FORMAT)


def cookie_time_to_str(value: datetime) -> str:
    """
    cast datetime object into a string
    :param value: datetime input
    :return: Date formatted string (if hour, minute and seconds of input is 0), Timestamp formatted if not
    """
    if value.hour == 0 and value.minute == 0 and value.second == 0:
        return value.strftime(COOKIE_DATE_FORMAT)
    return value.strftime(COOKIE_TIMESTAMP_FORMAT)


def convert_counter_to_str(counter: Counter, partial_time_data: dict = None) -> str:
    """
    encode Counter object into a string to be saved in cookie
    :param counter: input value
    :param partial_time_data: partial_timings dictionary (if presents) to be saved along side element pairs
    :return: string to be saved in cookie
    """

    key_values = []
    for key, value in counter.items():
        pair_str = str(key) + PAIR_SEPARATOR + str(value)
        if partial_time_data and key in partial_time_data:
            pair_str = cookie_time_to_str(partial_time_data[key]) + PARTIAL_TIME_SEPARATOR + pair_str
        key_values.append(pair_str)
    value_str = SPLITTER.join(key_values)
    return value_str


def convert_str_to_counter(value_str: str, age_days: int = None, return_partial_times: bool = False):
    """
    parse cookie's string into dictionary, preferably Counter object
    :param value_str: cookie's value in string format
    :param age_days: element's age (if not None indicates cookie is using partial timing)
    :param return_partial_times: whether to return dictionary of element ids and partial times as well or not
    :return: dictionary if using multiple pairs | Counter if it's a list or two-pairs |
    + partial timings dict if 'return_partial_times' is True
    """

    if not value_str:
        return Counter()

    # removing timestamp from beginning of cookie
    value_str = str(list(value_str.split(TIME_SEPARATOR))[-1])

    # cookie_with_count = '1~5|2~10|3~9'
    # cookie_without_counts = '1|2|1|1|3|1|2'
    # cookie_with_partial_time = '2017-07-11$1~5|2017-07-10$2~10|2017-07-09$3~9'
    extracted_dict = {}
    countless_list = []
    counter_compatible = True
    partial_time_data = {}
    if value_str is not None:
        for cookie_separated_by_split in value_str.split(SPLITTER):

            partial_time = None
            if PARTIAL_TIME_SEPARATOR in cookie_separated_by_split:
                """
                check partial time for each item, if item has expired will ignore it
                2017-07-09$3~9 => if more seconds passed from July9 than 'age_seconds' ignore the item
                """
                partial_time_str = cookie_separated_by_split.split(PARTIAL_TIME_SEPARATOR)[0]
                cookie_separated_by_split = cookie_separated_by_split.split(PARTIAL_TIME_SEPARATOR)[-1]
                partial_time = cookie_str_to_time(partial_time_str)
                if age_days and (datetime.now() - partial_time).days > age_days:
                    # expired partial time
                    continue
            if PAIR_SEPARATOR in cookie_separated_by_split:
                """
                item is a pair 1~5 or 1~5~2
                if only two pairs are in a split, they will turn into a key-value for Counter object {1:5}
                if not, all remaining pairs will be in an array for the key: {1:[5,2]}
                """
                cookie_pairs = cookie_separated_by_split.split(PAIR_SEPARATOR)  # type: list
                try:
                    pair_key = int(cookie_pairs[0])
                except ValueError:
                    pair_key = cookie_pairs[0]
                if len(cookie_pairs) == 2:
                    if pair_key in extracted_dict:
                        extracted_dict[pair_key] += int(cookie_pairs[1])
                    else:
                        extracted_dict[pair_key] = int(cookie_pairs[1])
                elif len(cookie_pairs) > 2:
                    # a list as value for a dictionary key cannot be casted to Counter object
                    counter_compatible = False
                    extracted_dict[pair_key] = []
                    for i in range(1, len(cookie_pairs)):
                        extracted_dict[pair_key].append(cookie_pairs[i])
            else:
                """
                item separated by split has no pairs, it is a single line list like '1|2|1|1|3|1|2'
                """
                try:
                    pair_key = int(cookie_separated_by_split)
                except ValueError:
                    pair_key = cookie_separated_by_split
                countless_list.append(pair_key)

            if partial_time:
                # add partial time per key in a separated dictionary
                partial_time_data[pair_key] = partial_time

        if len(countless_list) > 0:
            """
            a list created out of items separated by split will be casted to Counter object
            """
            extracted_dict = Counter(countless_list)

    if counter_compatible:
        extracted_dict = Counter(extracted_dict)
        """
        the only way this function won't return Counter object is when items in a split has more than 2 pairs
        like: '1~5~2|2~10~4~3|3~9'
        """

    if return_partial_times:
        return extracted_dict, partial_time_data
    return extracted_dict
