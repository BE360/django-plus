from collections import Counter

from django_plus.cookie_helper import cookie_classes, utils


class CounterCookie(cookie_classes.SimpleCookie):

    def set(self, counter, append=False):
        """
        :param counter: a counter
        :param append:
        :return:
        """

        counter_value = self.get()

        if not append or counter_value is None:
            counter_value = counter

        elif counter is not None:
            counter_value += counter

        str_value = None

        if counter_value is not None:
            str_value = utils.convert_counter_to_str(counter_value)

        super(CounterCookie, self).set(str_value)

    def get(self, age_days=None):

        if self.str_value is not None:
            counter = utils.convert_str_to_counter(self.str_value, age_days=age_days)

            if not isinstance(counter, Counter):
                return Counter()

            else:
                return counter

        else:
            return Counter()
