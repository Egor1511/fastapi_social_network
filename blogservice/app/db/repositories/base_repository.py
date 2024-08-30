from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError
