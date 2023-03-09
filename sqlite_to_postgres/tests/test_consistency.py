from config import POSTGRESQL_DSN, SQLITE_DB_PATH, TABLES_INFO

from context_managers import psycopg2_conn_context, sqlite3_conn_context

from dotenv import load_dotenv

load_dotenv()


def test_tables_count():
    with sqlite3_conn_context(SQLITE_DB_PATH) as sqlite_cursor:
        with psycopg2_conn_context(POSTGRESQL_DSN) as psycopg2_cursor:

            for table_info in TABLES_INFO:
                table_name = table_info.table_name
                schema_name = table_info.schema_name

                sqlite_cursor.execute(f'SELECT COUNT(id) FROM {table_name};')
                psycopg2_cursor.execute(f'SELECT COUNT(id) FROM {schema_name}.{table_name};')

                assert sqlite_cursor.fetchone() == psycopg2_cursor.fetchone()


def test_tables_fields():
    with sqlite3_conn_context(SQLITE_DB_PATH) as sqlite_cursor:
        with psycopg2_conn_context(POSTGRESQL_DSN) as psycopg2_cursor:

            for table_info in TABLES_INFO:
                table_name = table_info.table_name
                schema_name = table_info.schema_name
                columns = table_info.sqlite_columns

                testing_fields = ', '.join(columns)

                sqlite_cursor.execute(f'SELECT {testing_fields} FROM {table_name};')
                sqlite_data = set(sqlite_cursor.fetchall())

                psycopg2_cursor.execute(f'SELECT {testing_fields} FROM {schema_name}.{table_name};')
                psql_data = set(psycopg2_cursor.fetchall())

                assert sqlite_data == psql_data


def test_tables_exist():
    with psycopg2_conn_context(POSTGRESQL_DSN) as psycopg2_cursor:
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='content'"
        psycopg2_cursor.execute(sql)
        tables = set(table[0] for table in psycopg2_cursor.fetchall())
        assert tables == set(t.table_name for t in TABLES_INFO)
