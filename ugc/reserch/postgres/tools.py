import itertools


def read_lines_in_batches(file_path, batch_size):
    with open(file_path, 'r') as file:
        lines = list(itertools.islice(file, batch_size))
        while lines:
            yield lines
            lines = list(itertools.islice(file, batch_size))
