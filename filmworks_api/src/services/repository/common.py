import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_list(self, *args, **kwargs):
        pass
