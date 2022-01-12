import sys
import eel
import vars
import threading
import pickle
from musicqueue import MusicQueue
from repeat import RepeatState
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
from mediaplayer_state import MediaState
from htmlengine import HtmlEngine


START = time.perf_counter()
TRACKS_PATH_LIST = []
TRACKS = []
mediaPlayer = MediaPlayer()
mediaPlayer.setVolume(50)
INDEX = -1
HOST = '127.0.0.1'
PORT = 5911
FILESERVER_HOST = '127.0.0.1'
FILESERVER_PORT = 1984
INVALID_CHARACTERS = '/\\:*?"<>|'
repeat = RepeatState.RepeatNone
music_queue = MusicQueue()

eel.browsers.set_path('electron', 'node_modules/electron/dist/electron')

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
    cover_name = result.get("album")
    if cover_name == 'Unknown Album':
        cover_name = result.get('title')
    cover = os.path.join(
        vars.COVER_PATH, remove_invalid_chars(f'{ cover_name }.jpg'.strip()))
    if cover not in list(COVERS.keys()):
        COVERS[cover] = result['image']
    if result['image'] is not None:
        result['image'] = f'http://{FILESERVER_HOST}:{FILESERVER_PORT}' + cover
    else:
        result['image'] = None
    TRACKS.append(result)

with ThreadPoolExecutor() as executor:
    executor.map(save_album_art, list(COVERS.keys()), list(COVERS.values()))

del COVERS

LIBRARY = Library(TRACKS)

with open('/home/sidhu/Desktop/temp.pickle', 'wb') as f:
    pickle.dump(LIBRARY, f)

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
    if len(TRACKS) == 0:
        return False
    path = TRACKS[index].get('path')
    if os.path.exists(path):
        mediaPlayer.setMedia(path)
        mediaPlayer.play()
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


@eel.expose
def set_album_content(album):
    pass
    # album_data = LIBRARY.get_album_by_name(album)
    # return generate_album_template(album_data)

@eel.expose
def set_repeat_state(state):
    global repeat
    repeat = RepeatState(state)

@eel.expose
def get_repeat_state():
    return repeat.value


FILESERVER = multiprocessing.Process(target=start_fileserver, args=(FILESERVER_HOST, FILESERVER_PORT,))
FILESERVER.start()


def close_callback(route, websockets):
    if not websockets:
        kill_fileserver(FILESERVER_HOST, FILESERVER_PORT)
        FILESERVER.terminate()
        exit()


def onMediaPlayerTimeChangedCallback():
    duration = int(mediaPlayer.getTime() / 1000)
    if duration == -1:
        return
    eel.update_seekbar(duration)
    return


def onMediaStateChangedCallback():
    state = mediaPlayer.getState()
    if state.value == MediaState.Buffering.value:
        return
    elif state.value == MediaState.NothingSpecial.value:
        return
    elif state.value == MediaState.Opening.value:
        return
    elif state.value == MediaState.Playing.value:
        eel.set_playPause(True)
        return
    elif state.value == MediaState.Paused.value:
        eel.set_playPause(False)
        return
    elif state.value == MediaState.Stopped.value:
        eel.set_playPause(False)
        return
    elif state.value == MediaState.Error.value:
        return
    else:
        return


def onMediaPlayerEndReachedCallback():
    if repeat == RepeatState.RepeatNone:
        next_track()
    elif repeat == RepeatState.RepeatAll:
        next_track()
    elif repeat == RepeatState.RepeatOne:
        play_track(INDEX)
    sys.exit()
    return

def onMediaPlayerMediaChangedCallback():
    eel.set_playing_metadata(get_playing_metadata())
    return


mediaPlayer.setOnMediaPlayerTimeChangedCallback(onMediaPlayerTimeChangedCallback)
mediaPlayer.setOnMediaStateChangedCallback(onMediaStateChangedCallback)
mediaPlayer.setOnMediaPlayerEndReachedCallback(onMediaPlayerEndReachedCallback)
mediaPlayer.setOnMediaPlayerMediaChangedCallback(onMediaPlayerMediaChangedCallback)


eel.start(
    'templates/index.html',
    mode='electron',
    port=PORT,
    jinja_templates='templates',
    jinja_global=jinja_globals,
    block=True,
    close_callback=close_callback,
)

FINISH = time.perf_counter()
print(f'Finished in {FINISH - START}s.')
