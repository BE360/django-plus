from django_plus.cookie_helper.cookie_classes import SimpleCookie


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
