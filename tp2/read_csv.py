import numpy as np


def fuse_values(line: list[str]):
    res, value = [], []
    for value_part in line:
        if value_part.startswith('"'):
            value.append(value_part)
        elif value and value_part.endswith('"'):
            value.append(value_part)
            res.append(','.join(value)[1:-1])
            value = []
        elif value:
            value.append(value_part)
        else:
            res.append(value_part)
    return res


def read_csv(file):
    with open(file, 'r') as csv:
        data = csv.read()
    lines = data.split('\n')
    lines = map(lambda line: line.split(','), lines)
    lines = map(lambda line: fuse_values(line), lines)
    return list(lines)


_float = lambda x: float(str.lower(x).replace(',', '.'))


def get_ephemeride():
    data = read_csv('../csvs/Ephemerides1.csv')
    data[:] = map(lambda line: [_float(x) for x in line], data[1:-1])
    return np.array(data)


def get_pseudodist():
    data = read_csv('../csvs/Pseudodist1.csv')
    data[:] = map(lambda line: [_float(x) for x in line], data[:-1])
    return np.array(data)


if __name__ == '__main__':
    get_pseudodist()
    get_ephemeride()