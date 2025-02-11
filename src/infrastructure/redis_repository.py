import redis
from domain.repositories import RedisRepositoryInterface

class RedisRepository(RedisRepositoryInterface):
    def __init__(self, host, port, password):
        self.redis_client = redis.Redis(host=host, port=port, password=password, decode_responses=True)

    def save(self, key, data):
        self.redis_client.hset(key, mapping=data)
