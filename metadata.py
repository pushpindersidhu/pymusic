import os.path

from tinytag import TinyTag


class Metadata:

    def __init__(self, file, image=False) -> None:
        self.path = file
        self.tags = TinyTag.get(file, image=image)

    def album(self):
        album = self.tags.album
        if album is None:
            return "Unknown Album"
        else:
            return album

    def artist(self):
        artist = self.tags.artist
        if artist is None:
            return "Unknown Artist"
        else:
            return artist

    def album_artist(self):
        album_artist = self.tags.albumartist
        if album_artist is None:
            return self.artist()
        else:
            return album_artist

    def bitrate(self):
        return self.tags.bitrate

    def channels(self):
        return self.tags.channels

    def comment(self):
        comment = self.tags.comment
        if comment is None:
            return ""
        else:
            return comment

    def composer(self):
        composer = self.tags.composer
        if composer is None:
            return ""
        else:
            return composer

    def disc(self):
        disc = self.tags.disc
        if disc is None:
            return ""
        else:
            return disc

    def disc_total(self):
        disc_total = self.tags.disc_total
        if disc_total is None:
            return ""
        else:
            return disc_total

    def duration(self):
        return self.tags.duration

    def extra(self):
        return self.tags.extra

    def filesize(self):
        return self.tags.filesize

    def genre(self):
        genre = self.tags.genre
        if genre is None:
            return ""
        else:
            return genre

    def get_image(self):
        return self.tags.get_image()

    def samplerate(self):
        return self.tags.samplerate

    def title(self):
        title = self.tags.title
        if title is None:
            title, _ = os.path.splitext(os.path.basename(self.path))
            return title
        else:
            return title

    def track(self):
        track = self.tags.track
        if track is None:
            return ""
        else:
            return track

    def track_total(self):
        track_total = self.tags.track_total
        if track_total is None:
            return ""
        else:
            return track_total

    def year(self):
        year = self.tags.year
        if year is None:
            return ""
        else:
            return year

    def close(self):
        del self.tags

    def to_dict(self):
        return {
            'path': self.path,
            'album': self.album(),
            'artist': self.artist(),
            'album_artist': self.album_artist(),
            'bitrate': self.bitrate(),
            'channels': self.channels(),
            'comment': self.comment(),
            'composer': self.composer(),
            'disc': self.disc(),
            'disc_total': self.disc_total(),
            'duration': self.duration(),
            'extra': self.extra(),
            'filesize': self.filesize(),
            'genre': self.genre(),
            'image': self.get_image(),
            'sample_rate': self.samplerate(),
            'title': self.title(),
            'track': self.track(),
            'track_total': self.track_total(),
            'year': self.year(),
        }


if __name__ == '__main__':
    import json

    metadata = Metadata(
        '/home/sidhu/Music/[MP3DOWNLOAD.TO] Sher Rann Vich Lalkaare Maarda (CHAMKAUR SAHIB JUNG) - Kam Lohgarh Ft. SOHI BROS-320k.mp3')
    print(json.dumps(metadata.to_dict(), indent=4))
