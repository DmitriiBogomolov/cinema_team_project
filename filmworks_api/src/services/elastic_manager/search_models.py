from src.api.v1.common import PaginationParams


class Search:
    """Basic class for aggregate elasticsearch parameters"""
    def __init__(self, sort=None, pp: PaginationParams | None = None):
        self.query = {}
        self.set_sort(sort)
        self.set_pagination(pp)

    def set_sort(self, condition: str) -> None:
        """
        Translates sort condition.
            Parameters:
                condition: Sort condition string in API format
                           like '-imdb_rating'.
            Side effect:
                Set sort in Elastic format to a Search object.
        """
        if not condition:
            return
        elif condition[0] == '-':
            self.sort = {condition[1:]: 'desc'}
        else:
            self.sort = {condition: 'asc'}

    def set_pagination(self, pp: PaginationParams | None = None) -> None:
        """Set pagination params to a Search object"""
        if not pp:
            return
        self.size = pp.page_size
        self.from_ = (pp.page_number-1) * pp.page_size

    def get_search_params(self) -> dict:
        """Returns dict of parameters for searching through the ElasticSearch driver"""
        dic = self.__dict__
        if dic['query'] == {}:
            dic['query'] = None

        return dic


class FilmSearch(Search):
    """
    Concrete classes extends search parameters, for example:
    search by index and construct filtering parameters.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = 'movies'

    def add_multi_match_query(self, query: str) -> None:
        if query:
            self.query['multi_match'] = {
                'query': query,
                'fields': [
                    'title^3',
                    'description',
                    '*_names'
                ]
            }

    def add_nested_genre_query(self, genre_id: str) -> None:
        if genre_id:
            self.query['nested'] = {
                'path': 'genres',
                'query': {
                    'match': {'genres.id': genre_id}
                }
            }

    def add_by_ids_query(self, values: list[str]) -> None:
        if values:
            self.query['ids'] = {'values': values}


class PersonSearch(Search):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = 'persons'

    def add_match_query(self, full_name: str) -> None:
        if full_name:
            self.query['match'] = {'full_name': full_name}


class GenreSearch(Search):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = 'genres'
