from django_plus.cookie import utils


class SimpleCookie:

    __value = None  # typing str

    @property
    def str_value(self) -> str:
        return self.__value

    def __init__(self, stored_key, raw_value, encrypt_value=False, age_seconds=None, domain=None):
        self.encrypt_value = encrypt_value
        self.age_seconds = age_seconds
        self.domain = domain
        self.stored_key = stored_key

        self.dirty = False  # should be set in cookie

        if raw_value is not None:
            self.__value = utils.cookie_decrypt(raw_value, encryption=encrypt_value)

    def set(self, value, **kwargs):
        self.__value = value
        self.dirty = True

    def get(self, **kwargs):
        return self.str_value

    def attach_to(self, response):
        if self.dirty:

            if self.str_value is None:
                response.delete_cookie(self.stored_key)

            else:
                response.set_cookie(
                    key=self.stored_key,
                    value=utils.cookie_encrypt(self.str_value, encryption=self.encrypt_value),
                    domain=self.domain,
                    max_age=self.age_seconds
                )

    def is_empty(self):
        return self.str_value is None
