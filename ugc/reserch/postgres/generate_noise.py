import uuid
from datetime import datetime


def generate_noise(len):
    with open('noise.txt', 'w') as f:
        start_time = datetime.now()

        for i in range(len):
            f.write(
                f'{uuid.uuid4()}, {uuid.uuid4()}, {uuid.uuid4()},'
                '100, 2000, 2023-07-07' + '\n'
            )
            print(i)
            print(datetime.now() - start_time)


if __name__ == "__main__":
    generate_noise(1000000)
