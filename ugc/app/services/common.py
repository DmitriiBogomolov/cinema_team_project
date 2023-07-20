from fastapi import Query


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
        """Включать ли сортировку в запрос"""
        return bool(self.list)
