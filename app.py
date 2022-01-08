import eel
import vars
import os
import eel.browsers
import time
import multiprocessing
import random
from mediaplayer import MediaPlayer
from scan import scan
from concurrent.futures import ThreadPoolExecutor
from metadata import Metadata
from library import Library
from start_fileserver import start_fileserver
from port_availability import port_availability
from kill_fileserver import kill_fileserver
from playback_status import PlaybackStatus

START = time.perf_counter()
TRACKS_PATH_LIST = []
TRACKS = []
mediaPlayer = MediaPlayer()
INDEX = -1
HOST = '127.0.0.1'
PORT = 5911
FILESERVER_HOST = '127.0.0.1'
FILESERVER_PORT = 1984
INVALID_CHARACTERS = '/\\:*?"<>|'

while not port_availability(HOST, PORT):
    PORT = random.randint(1000, 65000)
while not port_availability(FILESERVER_HOST, FILESERVER_PORT):
    FILESERVER_PORT = random.randint(1000, 65000)


def remove_invalid_chars(filename: str) -> str:
    for invalid_char in INVALID_CHARACTERS:
        filename = filename.replace(invalid_char, '')
    return filename


def save_album_art(path, img_binaries):
    if not os.path.exists(path):
        if img_binaries is not None:
            with open(path, mode='wb') as img:
                img.write(img_binaries)


def duration_to_str(duration):
    minutes = int(duration / 60)
    secs = int(duration % 60)
    return ("0" if minutes < 10 else "") + str(minutes) + ":" + ("0" if secs < 10 else "") + str(secs)


for directory in vars.DIRS:
    TRACKS_PATH_LIST.extend(scan(directory))

with ThreadPoolExecutor() as executor:
    results = executor.map(lambda file: Metadata(
        file, image=True).to_dict(), TRACKS_PATH_LIST)

COVERS = {}

for i, result in enumerate(results):
    result['id'] = i + 1
    result['formatted_duration'] = duration_to_str(result['duration'])
    cover = os.path.join(
        vars.COVER_PATH, remove_invalid_chars(f'{result.get("album")}.jpg'.strip()))
    if cover not in list(COVERS.keys()):
        COVERS[cover] = result['image']
    result['image'] = f'http://{FILESERVER_HOST}:{FILESERVER_PORT}' + cover
    TRACKS.append(result)

with ThreadPoolExecutor() as executor:
    executor.map(save_album_art, list(COVERS.keys()), list(COVERS.values()))

del COVERS

LIBRARY = Library(TRACKS)

jinja_globals = {
    'title': 'Sidhu',
    'TRACKS': TRACKS,
    'LIBRARY': LIBRARY,
}

eel.init('web')


@eel.expose
def play_track(index):
    global INDEX
    INDEX = index
    if mediaPlayer.isPlaying():
        mediaPlayer.stop()
    path = TRACKS[index].get('path')
    if os.path.exists(path):
        mediaPlayer.setMedia(path)
        mediaPlayer.play()
        # noinspection PyUnresolvedReferences
        eel.set_playPause()
        # noinspection PyUnresolvedReferences
        eel.set_playing_metadata(get_playing_metadata())
        return True
    else:
        return False


@eel.expose
def get_playing_metadata():
    if INDEX == -1:
        return
    else:
        return TRACKS[INDEX]


@eel.expose
def is_playing():
    return mediaPlayer.isPlaying()


@eel.expose
def init():
    play_track(0)
    play_pause()


@eel.expose
def complete():
    mediaPlayer.stop()


@eel.expose
def play_pause():
    if INDEX == -1:
        play_track(0)
    else:
        if mediaPlayer.isPlaying():
            mediaPlayer.pause()
        else:
            mediaPlayer.unpause()


@eel.expose
def next_track():
    if INDEX == len(TRACKS) - 1:
        play_track(0)
    else:
        play_track(INDEX + 1)


@eel.expose
def previous_track():
    if INDEX == 0:
        play_track(len(TRACKS) - 1)
    else:
        play_track(INDEX - 1)


@eel.expose
def set_volume(volume):
    mediaPlayer.setVolume(int(volume))


@eel.expose
def get_volume():
    return mediaPlayer.getVolume()


@eel.expose
def get_total_duration():
    return int(TRACKS[INDEX]['duration'])


@eel.expose
def get_duration():
    duration = mediaPlayer.getTime()
    print(mediaPlayer.getPosition())
    if mediaPlayer.getPosition() == -1:
        complete()
        return 0
    duration = int(duration / 1000)
    return duration


@eel.expose
def seek_to(position):
    position = (int(position * 100_000_000) / 10_000_000_000)
    mediaPlayer.setPosition(position)


@eel.expose
def data():
    with open(vars.DATA_PATH) as f:
        return f.read()


@eel.expose
def data_path():
    return vars.DATA_PATH


FILESERVER = multiprocessing.Process(target=start_fileserver, args=(FILESERVER_HOST, FILESERVER_PORT,))
FILESERVER.start()


def close_callback(route, websockets):
    if not websockets:
        kill_fileserver(FILESERVER_HOST, FILESERVER_PORT)
        FILESERVER.terminate()
        exit()


eel.start(
    'templates/index.html',
    port=PORT,
    jinja_templates='templates',
    jinja_global=jinja_globals,
    block=True,
    close_callback=close_callback,
)

FINISH = time.perf_counter()
print(f'Finished in {FINISH - START}s.')
