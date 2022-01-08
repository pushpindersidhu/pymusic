import enum
from vlc import State


class MediaState(enum.Enum):
    NothingSpecial = State.NothingSpecial
    Opening = State.Opening
    Buffering = State.Buffering
    Playing = State.Playing
    Paused = State.Paused
    Stopped = State.Stopped
    Ended = State.Ended
    Error = State.Error
