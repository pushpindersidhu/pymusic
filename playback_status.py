import enum


class PlaybackStatus(enum.Enum):
    STOPPED = -1
    PLAYING = 1
    PAUSED = 0
