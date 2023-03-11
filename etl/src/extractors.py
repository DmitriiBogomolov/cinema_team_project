"""
Provides a function to preform query_str and making query
that returns a statable data generator.
    - extract_query_statable
"""


import datetime
from typing import List

from psycopg2.extras import RealDictRow

from logger import logger
from psql import PSQLManager
from state import State, state


class StatebleGenerator:
    """
    Gets the generator and saves state during iteration.

    __next__ will set the keyword state for the:
                  minimal 'modified' field value of the data portion objects.

    """
    def __init__(self, data_generator, state: State, keyword: str):
        self.data_generator = data_generator
        self.state = state
        self.keyword = keyword
        self.max_modified = None

    def __iter__(self):
        return self

    def __next__(self) -> List[RealDictRow]:
        try:
            data = next(self.data_generator)

            modified_set = [item['modified'] for item in data if item['modified']]

            if modified_set:
                min_modifided = min(modified_set)
                self.max_modified = max(modified_set)
                self.state.set_state(self.keyword, str(min_modifided))

            return data

        except StopIteration:
            logger.info('Stop iteration from the query data collection')

            if self.max_modified:
                logger.info('Saving control state.')

                tricky_dt = self.max_modified + datetime.timedelta(milliseconds=500)

                self.state.set_state(self.keyword, str(tricky_dt))
            raise StopIteration


def extract_query_statable(keyword: str, query_str: str, psql_manager: PSQLManager) -> StatebleGenerator:
    """
    Preform SQL query string, making query.
    Start fetching from current state value.
    """
    logger.info(f'Starting extract query from {keyword}.')

    state_value = state.get_state(keyword) or '1000-10-10'
    query_str = query_str.replace('{%s}' % keyword, "'%s\'" % state_value)

    data_generator = psql_manager.get_execution_generator(query_str)
    generator = StatebleGenerator(data_generator, state, keyword)

    return generator
