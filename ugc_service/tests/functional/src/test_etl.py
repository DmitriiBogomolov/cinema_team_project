import time
import os
from dotenv import load_dotenv
from tests.functional.test_data.generate_date_for_kafka import generate_test_data

load_dotenv()

BATCH_SIZE = int(os.getenv('TEST_BATCH_SIZE'))


def test_count_row(write_to_kafka, client_clickhouse):
    data = generate_test_data(BATCH_SIZE)
    write_to_kafka(data, 'views')
    time.sleep(1)
    number = client_clickhouse.execute('SELECT count() FROM events.views')
    assert number[0][0] == BATCH_SIZE
