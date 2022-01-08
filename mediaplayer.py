import vlc
from playback_status import PlaybackStatus


class MediaPlayer:

    onMediaPlayerTimeChanged = None
    onMediaPlayerPositionChanged = None
    onMediaDurationChanged = None
    onMediaStateChanged = None
    onMediaPlayerEndReached = None
    onMediaPlayerMediaChanged = None
    onMediaPlayerPaused = None
    onMediaPlayerPlaying = None
    onMediaPlayerMuted = None
    onMediaPlayerUnmuted = None
    onMediaPlayerStopped = None
    onMediaPlayerPausableChanged = None

    def __init__(self) -> None:
        self.instance = vlc.Instance()
        self.mediaPlayer = self.instance.media_player_new()
        self.eventManager = self.mediaPlayer.event_manager()
        self.media = None
        self.playbackstatus = PlaybackStatus.STOPPED

    def setMedia(self, mrl):
        self.media = self.instance.media_new(mrl)
        self.mediaPlayer.set_media(self.media)

    def release(self):
        self.media.release()
        self.mediaPlayer.release()

    @vlc.callbackmethod
    def onMediaPlayerTimeChangedCallback(self, event):
        if self.onMediaPlayerTimeChanged is not None:
            self.onMediaPlayerTimeChanged()

    def setOnMediaPlayerTimeChangedCallback(self, callback):
        self.eventManager.event_attach(vlc.EventType.MediaPlayerTimeChanged,
                                       self.onMediaPlayerTimeChangedCallback)
        self.onMediaPlayerTimeChanged = callback

    @vlc.callbackmethod
    def onMediaPlayerPositionChangedCallback(self, event):
        if self.onMediaPlayerPositionChanged is not None:
            self.onMediaPlayerPositionChanged()

    def setOnMediaPlayerPositionChangedCallback(self, callback):
        self.eventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged,
                                       self.onMediaPlayerPositionChangedCallback)
        self.onMediaPlayerPositionChanged = callback

    @vlc.callbackmethod
    def onMediaDurationChangedCallback(self, event):
        if self.onMediaDurationChanged is not None:
            self.onMediaDurationChanged()

    def setOnMediaDurationChangedCallback(self, callback):
        self.eventManager.event_attach(vlc.EventType.MediaDurationChanged,
                                       self.onMediaDurationChangedCallback)
        self.onMediaDurationChanged = callback

    @vlc.callbackmethod
    def onMediaStateChangedCallback(self, event):
        if self.onMediaStateChanged is not None:
            self.onMediaStateChanged()

    def setOnMediaStateChangedCallback(self, callback):
        self.eventManager.event_attach(vlc.EventType.MediaStateChanged,
                                       self.onMediaStateChangedCallback)
        self.onMediaStateChanged = callback

    @vlc.callbackmethod
    def onMediaPlayerEndReachedCallback(self, event):
        if self.onMediaPlayerEndReached is not None:
            self.onMediaPlayerEndReached()

    def setOnMediaPlayerEndReachedCallback(self, callback):
        self.eventManager.event_attach(vlc.EventType.MediaPlayerEndReached,
                                       self.onMediaPlayerEndReachedCallback)
        self.onMediaPlayerEndReached = callback

    @vlc.callbackmethod
    def onMediaPlayerMediaChangedCallback(self, event):
        if self.onMediaPlayerMediaChanged is not None:
            self.onMediaPlayerMediaChanged()

    def setOnMediaPlayerMediaChangedCallback(self, callback):
        self.eventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged,
                                       self.onMediaPlayerMediaChangedCallback)
        self.onMediaPlayerMediaChanged = callback

    def attachEvent(self, event_type, callback):
        self.eventManager.event_attach(event_type, callback)

    def play(self):
        self.mediaPlayer.play()
        self.playbackstatus = PlaybackStatus.PLAYING

    def stop(self):
        self.mediaPlayer.stop()
        self.playbackstatus = PlaybackStatus.STOPPED

    def restart(self):
        self.stop()
        self.play()

    def pause(self):
        self.mediaPlayer.pause()
        self.playbackstatus = PlaybackStatus.PAUSED

    def unpause(self):
        self.mediaPlayer.pause()
        self.playbackstatus = PlaybackStatus.PLAYING

    def getLength(self):
        self.mediaPlayer.get_length()

    def getState(self):
        self.mediaPlayer.get_state()

    def setVolume(self, volume):
        return self.mediaPlayer.audio_set_volume(volume)

    def getVolume(self):
        return self.mediaPlayer.audio_get_volume()

    def getPlaybackStatus(self):
        return self.playbackstatus

    def isPlaying(self):
        return self.playbackstatus == PlaybackStatus.PLAYING

    def setPosition(self, position):
        self.mediaPlayer.set_position(position)

    def getPosition(self):
        return self.mediaPlayer.get_position()

    def getTime(self):
        return self.mediaPlayer.get_time()

    def setTime(self, time_ms):
        self.mediaPlayer.set_time(time_ms)


if __name__ == '__main__':
    import time

    def onTimeChanged():
        print(mediaPlayer.getPosition())

    mediaPlayer = MediaPlayer()
    mediaPlayer.setOnMediaPlayerPositionChangedCallback(onTimeChanged)
    mediaPlayer.setMedia('/home/sidhu/Music/Sidhu/10. The Weeknd - Tears In The Rain.flac')
    mediaPlayer.setVolume(10)
    print("Volume: ", mediaPlayer.getVolume())
    mediaPlayer.play()
    mediaPlayer.setPosition(0.50)
    print('Playing at length: 50%')
    time.sleep(1)
    mediaPlayer.pause()
    print('Paused')
    time.sleep(1)
    print('Playing...')
    mediaPlayer.unpause()
    time.sleep(1)
    print('Restarting...')
    mediaPlayer.restart()
    print('Playing at time: 100s')
    mediaPlayer.setTime(50)
    print('Setting volume: 1')
    mediaPlayer.setVolume(0)
    time.sleep(1)
    print(mediaPlayer.getVolume())
    print(mediaPlayer.getLength())
    print(mediaPlayer.getPlaybackStatus())
    print(mediaPlayer.getPosition())
    print(mediaPlayer.isPlaying())
