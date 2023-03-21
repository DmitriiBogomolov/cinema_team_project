class PaginationParams:
    """Общие парамеры постраничного разбиения выдачи эндпоинтов API."""

    def __init__(self,
                 page_size: int = 50,
                 page_number: int = 1) -> None:
        self.page_size = page_size
        self.page_number = page_number
