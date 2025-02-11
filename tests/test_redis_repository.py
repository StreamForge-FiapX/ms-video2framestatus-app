import unittest
from unittest.mock import patch, MagicMock
from redis_repository import RedisRepository

class TestRedisRepository(unittest.TestCase):
    @patch('redis_repository.redis.Redis')
    def test_save(self, MockRedis):
        mock_redis = MagicMock()
        MockRedis.return_value = mock_redis

        redis_repo = RedisRepository('localhost', 6379, None)
        redis_repo.save('test_key', {"field": "value"})

        mock_redis.hset.assert_called_with('test_key', mapping={"field": "value"})

if __name__ == '__main__':
    unittest.main()
