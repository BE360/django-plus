from django_plus.cookie import CookieParam


def get_cookie_handler(cookies, cookie_params, default_cookie_domain=None):
    handler = {}

    for param in cookie_params:  # type: CookieParam

        raw_value = cookies.get(param.stored_key, None)

        domain = param.domain
        if domain is None:
            domain = default_cookie_domain

        handler[param.key] = param.cookie_class(
            param.stored_key,
            raw_value,
            encrypt_value=param.encrypt_value,
            age_seconds=param.age_seconds,
            domain=domain,
        )

    return handler
