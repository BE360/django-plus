from django_plus.fa import fa_convert
from ._generator_ import admin_field_generator


def number(verbose_name="", path_to_field=None, wrap_white_space=True, split_length=3,
           splitter=','):

    def function_changer(func, admin, instance):

        amount = func(admin, instance)

        if amount:
            num = fa_convert(str(amount))
        else:
            num = ""

        if len(num) > 0 and split_length > 0:
            num_reversed = num[::-1]
            num_reverse_char_inserted = splitter.join(
                num_reversed[i:i + split_length] for i in range(0, len(num), split_length)
            )
            num = num_reverse_char_inserted[::-1]

        return num

    return admin_field_generator(
        verbose_name=verbose_name,
        path_to_field=path_to_field,
        function_changer=function_changer,
        wrap_white_space=wrap_white_space
    )

