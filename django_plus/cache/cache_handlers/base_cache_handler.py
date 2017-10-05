import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)


class BaseCacheHandler:
    timeout = None
    key = None

    def get(self, *args, **kwargs):

        key = self.get_key(*args, **kwargs)

        if key is None:
            raise ValueError('Redis key cannot be None')

        data = cache.get(key)

        return data

    def set(self, data, *args, **kwargs):
        key = self.get_key(*args, **kwargs)
        timeout = self.get_timeout(*args, **kwargs)
        cache.set(key, data, timeout=timeout)

    def get_key(self, *args, **kwargs):
        return self.key

    def get_timeout(self, *args, **kwargs):
        return self.timeout
