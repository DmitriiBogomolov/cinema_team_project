from config import DATA_CHUNK, POSTGRESQL_DSN, SQLITE_DB_PATH, TABLES_INFO

from context_managers import psycopg2_conn_context, sqlite3_conn_context

from logger_config import logger

from manipulators import (get_data_from_sqlite, load_data_to_postgresql,
                          truncate_psql_table, create_schema)


def main():

    with sqlite3_conn_context(SQLITE_DB_PATH) as sqlite_conn:
        with psycopg2_conn_context(POSTGRESQL_DSN) as psycopg2_conn:
            sqlite_cursor = sqlite_conn.cursor()
            psycopg2_cursor = psycopg2_conn.cursor()

            create_schema(psycopg2_cursor)

            for table_info in TABLES_INFO:
                table_name = table_info.table_name
                schema_name = table_info.schema_name
                columns = table_info.sqlite_columns
                data_class = table_info.dataclass

                psql_table_name = f'{schema_name}.{table_name}'

                logger.info(f'Handle {psql_table_name}')

                truncate_psql_table(psycopg2_cursor, psql_table_name)

                for data in get_data_from_sqlite(sqlite_cursor, table_name, columns, data_class, DATA_CHUNK):
                    load_data_to_postgresql(psycopg2_cursor, psql_table_name, data)

            psycopg2_conn.commit()

    logger.info('Success')


if __name__ == '__main__':
    main()
