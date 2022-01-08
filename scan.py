import os
from vars import DIRS, SUPPORTED_EXTENSIONS


def scan(directory):
    scanned = []
    for path in os.listdir(directory):
        path = os.path.join(directory, path)
        if os.path.isdir(path):
            scanned.extend(scan(path))
        elif os.path.splitext(path)[1] in SUPPORTED_EXTENSIONS:
            scanned.append(path)
    return scanned


if __name__ == '__main__':
    for i in DIRS:
        print(len(scan(i)))
