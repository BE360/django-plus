

def str_periodic_inserter(target_str, parts_length, splitter, start_from_right=True):

    if start_from_right:
        target_str = target_str[::-1]

    result = splitter.join(
        target_str[i:i + parts_length] for i in range(0, len(target_str), parts_length)
    )

    if start_from_right:
        result = result[::-1]

    return result
