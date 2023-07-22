from dataclasses import dataclass

from fastapi import Query


@dataclass
class OperationResult:
    """Результат операции, возвращаемый из репозиториев"""

    target_id: str | None = None
    count: str | None = None

    def __bool__(self):
        return bool(self.target_id) or bool(self.count)


class SortParam:
    """Парсит строку сортировки"""
    def __init__(
            self,
            sort: str = Query(
                '',
                title='Sort string',
                max_length=3
            ),
    ):
        params = [param for param in sort.split('&') if param]
        self.list = [
            (p, 1) if not p.startswith('-')
            else (p.removeprefix('-'), -1)
            for p in params
        ]

    def __bool__(self):
        return bool(self.list)
