"""
Предоставляет базовый класс для обработки
запросов к MongoDB
"""

from abc import abstractmethod

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection
)

from app.models import BasicModel
from app.repositories.zcommon import (
    OperationResult,
    SortParam
)


class BaseRepository:
    """Базовый класс для обработки запросов к MongoDB"""
    db_name = 'ugc_db'
    default_sort = [('created_at', -1)]

    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo = mongo

    @property
    @abstractmethod
    def default_collection_name(self) -> str:
        """Наследники переопределяют коллекцию хранилища"""
        pass

    @property
    @abstractmethod
    def model_class(self) -> BasicModel:
        """Наследники переопределяют модель"""
        pass

    @property
    @abstractmethod
    def collection(self) -> AsyncIOMotorCollection:
        """Возвращает объект коллекции"""

        return (
            self.mongo[self.db_name]
                      [self.default_collection_name]
        )

    async def get_by_id(self, id: str) -> BasicModel:
        """Получить документ по ID"""
        doc = await (
            self.collection.find_one({'_id': str(id)})
        )

        return self.model_class(**doc) or None

    async def search(
        self,
        search: dict,
        sort: SortParam | None = None
    ) -> list[BasicModel]:
        """Выполняет поиск документов"""
        docs = await (
            self.collection
                .find(search)
                .sort(sort.list if sort else [('created_at', -1)])
        ).to_list(length=None)

        return [self.model_class(**doc)
                for doc in docs]

    async def add(
        self,
        model: BasicModel
    ) -> OperationResult:
        """Добавляет документ, соответствуютщий модели"""
        result = await self.collection.insert_one(model.to_doc())

        return OperationResult(
            target_id=result.inserted_id
        )

    async def count(
        self,
        search: dict
    ) -> int:
        """Количество документов по условию поиска"""

        return await (
            self.collection.count_documents(search)
        )

    async def average(
        self,
        search: dict,
        avg_field: str
    ) -> int:
        """Среднее значение полей документов по условию поиска"""
        result = await (
            self.collection.aggregate([
                {'$match': search},
                {
                    '$group': {
                        '_id': 'null',
                        'avg_val': {'$avg': f'${avg_field}'}
                    }
                }
            ])
        ).to_list(length=None)

        if not result:
            return -1
        return result[0]['avg_val']

    async def replace(
        self,
        search: dict,
        model: BasicModel
    ) -> OperationResult:
        """
        Заменяет (обновляет) документ по условию поиска
        соответствующим переданной модели
        """
        result = await (
            self.collection.replace_one(
                search, model.to_doc()
            )
        )

        return OperationResult(
            target_id=result.modified_count
        )

    async def delete(self, search: dict):
        """Удаляет документ по условию поиска"""
        result = await self.collection.delete_one(search)

        return OperationResult(
            count=result.deleted_count
        )
