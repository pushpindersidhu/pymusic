import json
import time
from concurrent.futures import ThreadPoolExecutor
import vars
import os
from metadata import Metadata
from scan import scan
import uuid

DATA = []

INVALID_CHARACTERS = '/\\:*?"<>|'


def remove_invalid_chars(filename : str) -> str:
    for invalid_char in INVALID_CHARACTERS:
        filename = filename.replace(invalid_char, '')
    return filename

def save_album_art(path, data):
    if not os.path.exists(path):
        if data != None:
            with open(path, mode='wb') as img:
                img.write(data)


def setup():

    if not os.path.exists(vars.LIBRARY_PATH):
        os.mkdir(vars.LIBRARY_PATH)

    if not os.path.exists(vars.COVER_PATH):
        os.mkdir(vars.COVER_PATH)

    audio_list = []
    for dir in vars.DIRS:
        audio_list.extend(scan(dir))

    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda file: Metadata(
            file, image=True).to_dict(), audio_list)

    for i, result in enumerate(results):
        result['id'] = i + 1
        DATA.append(result)

    cover_path = []
    cover_data = []
    for index, path in enumerate([os.path.join(
            vars.COVER_PATH, remove_invalid_chars((f'{ data.get("album", str(uuid.uuid4())) }.jpg').strip())) for data in DATA]):
        if path not in cover_path:
            cover_path.append(path)
            cover_data.append(DATA[index]['image'])
        DATA[index]['image'] = os.path.join('Library/Covers', os.path.basename(path))

    with ThreadPoolExecutor() as executor:
        executor.map(save_album_art, cover_path, cover_data)

    with open(vars.DATA_PATH, 'w') as f:
        json.dump(DATA, f, indent=4)

    return DATA


if __name__ == '__main__':
    from time import perf_counter
    start = perf_counter()
    setup()
    finish = perf_counter()
    print(f'Finished in { finish - start }s.')
