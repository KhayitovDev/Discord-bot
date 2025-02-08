from abc import ABC, abstractmethod
from core.logger import logger


class Connection(ABC):
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    async def disconnect(self):
        try:
            await self._client.close()
        except TypeError:
            self._client.close()
        self._client = None
        self._instance = None
        logger.info(f"Disconnected from {self.__class__.__name__} server.")