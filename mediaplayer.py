import vlc
from playback_status import PlaybackStatus


class MediaPlayer:

    def __init__(self) -> None:
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.media = None
        self.playbackstatus = PlaybackStatus.STOPPED

    def set_media(self, mrl):
        self.media = self.instance.media_new(mrl)
        self.mediaplayer.set_media(self.media)

    def release(self):
        self.media.release()
        self.mediaplayer.release()

    def play(self):
        self.mediaplayer.play()
        self.playbackstatus = PlaybackStatus.PLAYING

    def stop(self):
        self.mediaplayer.stop()
        self.playbackstatus = PlaybackStatus.STOPPED

    def restart(self):
        self.stop()
        self.play()

    def pause(self):
        self.mediaplayer.pause()
        self.playbackstatus = PlaybackStatus.PAUSED

    def unpause(self):
        self.mediaplayer.pause()
        self.playbackstatus = PlaybackStatus.PLAYING

    def get_length(self):
        self.mediaplayer.get_length()

    def set_volume(self, volume):
        return self.mediaplayer.audio_set_volume(volume)

    def get_volume(self):
        return self.mediaplayer.audio_get_volume()

    def get_playbackstatus(self):
        return self.playbackstatus

    def is_playing(self):
        return self.playbackstatus == PlaybackStatus.PLAYING

    def set_position(self, position):
        self.mediaplayer.set_position(position)

    def get_position(self):
        return self.mediaplayer.get_position()

    def get_time(self):
        return self.mediaplayer.get_time()

    def set_time(self, time_ms):
        self.mediaplayer.set_time(time_ms)


if __name__ == '__main__':
    import time

    mediaPlayer = MediaPlayer()
    mediaPlayer.set_media('/home/sidhu/Music/Sidhu/10. The Weeknd - Tears In The Rain.flac')
    mediaPlayer.set_volume(10)
    print("Volume: ", mediaPlayer.get_volume())
    mediaPlayer.play()
    mediaPlayer.set_position(0.50)
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
    mediaPlayer.set_time(50)
    print('Setting volume: 1')
    mediaPlayer.set_volume(0)
    time.sleep(1)
    print(mediaPlayer.get_volume())
    print(mediaPlayer.get_length())
    print(mediaPlayer.get_playbackstatus())
    print(mediaPlayer.get_position())
    print(mediaPlayer.is_playing())
