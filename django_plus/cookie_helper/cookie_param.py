from django.conf import settings

from django_plus.cookie_helper import SimpleCookie


class CookieParam:

    def __init__(self, key, cookie_class=SimpleCookie, stored_key=None, encrypt_value=False, age=None, domain=None):
        self.key = key
        self.cookie_class = cookie_class
        self.stored_key = stored_key
        self.encrypt_value = encrypt_value
        self.age_seconds = age
        self.domain = domain

        if self.stored_key is None:
            self.stored_key = self.key

    @staticmethod
    def get_handler(cookies, cookie_params):

        handler = {}

        for param in cookie_params:  # type: CookieParam

            raw_value = cookies.get(param.stored_key, None)

            domain = param.domain
            if domain is None:
                domain = settings.COOKIE_DOMAIN_VIEW

            handler[param.key] = param.cookie_class(
                param.stored_key,
                raw_value,
                encrypt_value=param.encrypt_value,
                age_seconds=param.age_seconds,
                domain=domain,
            )

        return handler
