import unittest
from redis_repository_interface import RedisRepositoryInterface
from unittest.mock import MagicMock

class TestRedisRepositoryInterface(unittest.TestCase):
    def test_save(self):
        mock_repo = MagicMock(RedisRepositoryInterface)
        mock_repo.save("test_key", {"field": "value"})
        mock_repo.save.assert_called_with("test_key", {"field": "value"})

if __name__ == '__main__':
    unittest.main()
