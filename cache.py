import config
import redis


class Cache:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(config.Config.REDIS_URL)

    def get_product(self, product_title: str):
        return self.redis_client.get(product_title)

    def set_product(self, product_title: str, product_price: float):
        self.redis_client.set(product_title, product_price)
