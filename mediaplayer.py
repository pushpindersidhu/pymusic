from pygame import mixer


class MediaPlayer:

    def __init__(self) -> None:
        mixer.init()
        self.start = 0

    def load(self, path):
        mixer.music.load(path)

    def unload(self):
        mixer.music.unload()

    def play(self, loops=0, start=0.1, fade_ms=0):
        mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
        self.start = int(start * 1000)

    def rewind(self):
        return mixer.music.rewind()

    def stop(self):
        mixer.music.stop()

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()

    def fadeout(self, time=0):
        mixer.music.fadeout(time=time)

    def set_volume(self, volume):
        mixer.music.set_volume(volume)

    def get_volume(self):
        return mixer.music.get_volume()

    def is_playing(self):
        return mixer.music.get_busy()

    def set_pos(self, pos):
        mixer.music.set_pos(pos)

    def get_pos(self):
        return mixer.music.get_pos() + self.start

    def set_endevent(self, event):
        mixer.music.set_endevent(event)

    def get_endevent(self):
        mixer.music.get_endevent()


if __name__ == '__main__':
    import time
    from metadata import Metadata

    mediaPlayer = MediaPlayer()
    mediaPlayer.load('/home/sidhu/Music/Sidhu/10. The Weeknd - Tears In The Rain.flac')
    mediaPlayer.play(start=7 * 60 + 21.2)
    metadata = Metadata('/home/sidhu/Music/Sidhu/10. The Weeknd - Tears In The Rain.flac')
    print(int((metadata.duration()) * 1000))
    while True:
        print(mediaPlayer.start, '--', mediaPlayer.get_pos() + 1)
        if (mediaPlayer.start == mediaPlayer.get_pos() + 1):
            break

# 444742
