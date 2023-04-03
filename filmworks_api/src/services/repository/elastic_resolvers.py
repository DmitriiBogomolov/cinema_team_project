from src.api.v1.common import PaginationParams


class BasicParamsResolver():
    def __init__(self, params: dict) -> None:
        self.elastic_params = {}

        if params.get('sort'):
            self.elastic_params['sort'] = self.get_sort(params['sort'])

        if params.get('pp'):
            self.elastic_params['from_'] = self.get_from(params['pp'])
            self.elastic_params['size'] = self.get_size(params['pp'])

        query = self.get_query(params)
        if query:
            self.elastic_params['query'] = self.get_query(params)

    def get_sort(self, condition: str) -> dict:
        if condition[0] == '-':
            return {condition[1:]: 'desc'}
        else:
            return {condition: 'asc'}

    def get_from(self, pp: PaginationParams) -> int:
        return (pp.page_number-1) * pp.page_size

    def get_size(self, pp: PaginationParams) -> int:
        return pp.page_size

    def get_query(self, params: dict) -> None:
        return None

    def get_elastic_params(self) -> dict:
        return self.elastic_params


class MovieParamsResolver(BasicParamsResolver):
    def get_query(self, params: dict) -> dict:
        query = {}

        if params.get('movie'):
            query['multi_match'] = {
                'query': params['movie'],
                'fields': [
                    'title^3',
                    'description',
                    '*_names'
                ]
            }
        if params.get('genres'):
            query['nested'] = {
                'path': 'genres',
                'query': {
                    'match': {'genres.id': params['genres']}
                }
            }
        if params.get('by_ids'):
            query['ids'] = {'values': params['by_ids']}

        return query


class PersonParamsResolver(BasicParamsResolver):
    def get_query(self, params: dict) -> dict:
        query = {}

        if params.get('full_name'):
            query['match'] = {'full_name': params['full_name']}

        return query
