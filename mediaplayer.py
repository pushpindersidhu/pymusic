import vlc
import sys
import threading
from playback_status import PlaybackStatus
from mediaplayer_state import MediaState


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
        self.media = self.instance.media_new('')
        self.mediaEventManager = self.media.event_manager()
        self.volume = 50
        self.playbackstatus = PlaybackStatus.STOPPED


    def setMedia(self, mrl):
        self.mediaEventManager.event_detach(vlc.EventType.MediaStateChanged)
        self.media = self.instance.media_new(mrl)
        self.mediaEventManager = self.media.event_manager()
        self.setOnMediaStateChangedCallback(self.onMediaStateChanged)
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
        self.mediaEventManager.event_attach(vlc.EventType.MediaDurationChanged,
                                       self.onMediaDurationChangedCallback)
        self.onMediaDurationChanged = callback

    @vlc.callbackmethod
    def onMediaStateChangedCallback(self, event):
        if self.onMediaStateChanged is not None:
            thread = threading.Thread(target=self.onMediaStateChanged).start()
            del thread

    def setOnMediaStateChangedCallback(self, callback):
        self.mediaEventManager.event_attach(vlc.EventType.MediaStateChanged,
                                       self.onMediaStateChangedCallback)
        self.onMediaStateChanged = callback

    @vlc.callbackmethod
    def onMediaPlayerEndReachedCallback(self, event):
        if self.onMediaPlayerEndReached is not None:
            thread = threading.Thread(target=self.onMediaPlayerEndReached).start()
            del thread
            

    def setOnMediaPlayerEndReachedCallback(self, callback):
        self.eventManager.event_attach(vlc.EventType.MediaPlayerEndReached,
                                       self.onMediaPlayerEndReachedCallback)
        self.onMediaPlayerEndReached = callback

    @vlc.callbackmethod
    def onMediaPlayerMediaChangedCallback(self, event):
        if self.onMediaPlayerMediaChanged is not None:
            self.onMediaPlayerMediaChanged()

    def setOnMediaPlayerMediaChangedCallback(self, callback):
        self.eventManager.event_attach(vlc.EventType.MediaPlayerMediaChanged,
                                       self.onMediaPlayerMediaChangedCallback)
        self.onMediaPlayerMediaChanged = callback

    def attachEvent(self, event_type, callback):
        self.eventManager.event_attach(event_type, callback)

    def play(self):
        self.mediaPlayer.play()
        self.setVolume(self.volume)
        self.playbackstatus = PlaybackStatus.PLAYING

    def stop(self):
        self.mediaEventManager.event_detach(vlc.EventType.MediaStateChanged)
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
        return self.mediaPlayer.get_state()

    def setVolume(self, volume):
        self.volume = volume
        return self.mediaPlayer.audio_set_volume(volume)
        
    def getVolume(self):
        return self.mediaPlayer.audio_get_volume()

    def getPlaybackStatus(self):
        return self.playbackstatus

    def isPlaying(self):
        return self.getState().value == MediaState.Playing.value

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

    mediaPlayer = MediaPlayer()


    def onMediaPlayerTimeChangedCallback():
        print(mediaPlayer.getTime())
        return


    def onMediaStateChangedCallback():
        print('state', mediaPlayer.getState())
        return

    def reset():
        mediaPlayer.setMedia('/home/sidhu/Music/Sidhu/10. The Weeknd - Tears In The Rain.flac')
        mediaPlayer.play()


    def onMediaPlayerEndReachedCallback():
        print('calling end')
        reset()
        print(mediaPlayer.getState())
        sys.exit()
        


    def onMediaPlayerMediaChangedCallback():
        print('media changed')
        return

    def onMediaDurationChangedCallback():
        print('duration changed')
        return


    mediaPlayer.setOnMediaPlayerTimeChangedCallback(onMediaPlayerTimeChangedCallback)
    mediaPlayer.setOnMediaStateChangedCallback(onMediaStateChangedCallback)
    mediaPlayer.setOnMediaPlayerEndReachedCallback(onMediaPlayerEndReachedCallback)
    mediaPlayer.setOnMediaPlayerMediaChangedCallback(onMediaPlayerMediaChangedCallback)
    mediaPlayer.setOnMediaDurationChangedCallback(onMediaDurationChangedCallback)
    mediaPlayer.setMedia('/home/sidhu/Music/Sidhu/10. The Weeknd - Tears In The Rain.flac')
    mediaPlayer.play()
    mediaPlayer.setPosition(0.999)

    time.sleep(5)

    mediaPlayer.setVolume(50)
    mediaPlayer.play()
    mediaPlayer.restart()
    mediaPlayer.setTime(50)
    mediaPlayer.setVolume(0)
    time.sleep(1)
    print(mediaPlayer.getVolume())
    print(mediaPlayer.getLength())
    print(mediaPlayer.getPlaybackStatus())
    print(mediaPlayer.getPosition())
    print(mediaPlayer.isPlaying())
    input()
    
