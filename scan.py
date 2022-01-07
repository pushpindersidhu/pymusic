import os
from vars import DIRS, SUPPORTED_EXTENSIONS

def scan(dir):
    scanned = []
    for path in os.listdir(dir):
        path = os.path.join(dir, path)
        if os.path.isdir(path):
            scanned.extend(scan(path))
        elif os.path.splitext(path)[1] in SUPPORTED_EXTENSIONS:
            scanned.append(path)
    return scanned


if __name__=='__main__':
    for dir in DIRS:
        print(len(scan(dir)))