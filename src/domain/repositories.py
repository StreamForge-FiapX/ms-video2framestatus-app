from abc import ABC, abstractmethod

class RedisRepositoryInterface(ABC):
    @abstractmethod
    def save(self, key, data):
        pass
