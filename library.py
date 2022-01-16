import json


class Library:

    # Library Structure

    # library = [
    #     {
    #         'artist': 'Unknown Artist',
    #         'artist_image': None,
    #         'albums': [
    #             {
    #                 'album': 'Unknown Album',
    #                 'album_artist': 'Unknown Album Artist',
    #                 'album_art': None,
    #                 'year': 5911,
    #                 'track_total': 0,
    #                 'disc_total': 0,
    #                 'tracks': [
    #                     {
    #                         'path': None,
    #                         'id': 0,
    #                         'title': 'Unknown Title',
    #                         'artist': 'Unknown Artist',
    #                         'album': 'Unknown Album',
    #                         'genre': 'Unknown Genre',
    #                         'album_artist': 'Unknown Album Artist',
    #                         'composer': '',
    #                         'track': -1,
    #                         'total_tracks': -1,
    #                         'bitrate': -1,
    #                         'disc': -1,
    #                         'total_discs': -1,
    #                         'duration': -1,
    #                         'filesize': -1,
    #                         'samplerate': -1,
    #                         'year': -1,
    #                         'channels': -1,
    #                         'comment': None,
    #                         'album_art': None,
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # ]

    def __init__(self, tracks: list = None, library: list = None) -> None:
        
        if tracks is not None:
            
            self.tracks = tracks
            self.artists = []
            self.albums = []
            self.library = []

            for track in tracks:
                album_artist = track.get('album_artist')
                artist_image = track.get('image')
                album = track.get('album')
                if not self.artist_exists(album_artist):
                    self.artists.append(album_artist)
                    self.library.append(self.artist(album_artist, artist_image=artist_image))
                if not self.album_exists(album):
                    self.albums.append(album)
                    self.library[self.get_artist_index(album_artist)].get('albums').append(self.album(
                        album,
                        track.get('album_artist'),
                        track.get('image'),
                        track.get('year'),
                        track.get('track_total'),
                        track.get('disc_total'),
                    ))
                self.library[self.get_artist_index(album_artist)] \
                    .get('albums')[self.get_album_index(album, album_artist)] \
                    .get('tracks').append(track)

    def get_artist_index(self, artist):
        if artist in self.artists:
            return self.artists.index(artist)
        else:
            return -1

    def get_album_index(self, album_name, artist_name=None):
        if artist_name is not None:
            for index, temp in enumerate(self.library[self.get_artist_index(artist_name)].get('albums')):
                if temp.get('album') == album_name:
                    return index
            return -1
        else:
            for artist in self.artists:
                for index, album in enumerate(self.library[self.get_artist_index(artist)].get('albums')):
                    if album.get('album') == album_name:
                        return index
            return -1

    @staticmethod
    def artist(name, artist_image=None, albums=None):
        if albums is None:
            return {
                'artist': name,
                'artist_image': artist_image,
                'albums': []
            }
        else:
            return {
                'artist': name,
                'artist_image': artist_image,
                'albums': albums
            }

    @staticmethod
    def album(album, album_artist, album_art, year, track_total, disc_total, tracks=None):
        if tracks is None:
            return {
                'album': album,
                'album_artist': album_artist,
                'album_art': album_art,
                'year': year,
                'track_total': track_total,
                'disc_total': disc_total,
                'tracks': [],
            }
        else:
            return {
                'album': album,
                'album_artist': album_artist,
                'album_art': album_art,
                'year': year,
                'track_total': track_total,
                'disc_total': disc_total,
                'tracks': tracks,
            }

    @staticmethod
    def track(path, track_id, album, artist, album_artist, bitrate, channels, comment,
              composer, disc, disc_total, duration, extra, filesize, genre,
              image, sample_rate, title, track, track_total, year):
        return {
            'path': path,
            'id': track_id,
            'album': album,
            'artist': artist,
            'album_artist': album_artist,
            'bitrate': bitrate,
            'channels': channels,
            'comment': comment,
            'composer': composer,
            'disc': disc,
            'disc_total': disc_total,
            'duration': duration,
            'extra': extra,
            'filesize': filesize,
            'genre': genre,
            'image': image,
            'sample_rate': sample_rate,
            'title': title,
            'track': track,
            'track_total': track_total,
            'year': year,
        }

    def album_exists(self, album):
        return album in self.albums

    def artist_exists(self, artist):
        return artist in self.artists

    def get_library(self):
        return self.library

    def get_all_tracks(self):
        return self.tracks

    def get_all_artists_name(self):
        return self.artists

    def get_all_albums_name(self):
        return self.albums

    def get_all_albums(self):
        albums = []
        for artist in self.library:
            albums.extend(artist.get('albums'))
        return albums

    def get_album_by_name(self, name):
        for artist in self.library:
            for album in artist.get('albums'):
                if album.get('album') == name:
                    return album
        return None

    def get_artist_by_name(self, name):
        for artist in self.library:
            if artist.get('artist') == name:
                return artist
        return None

    def get_track_by_name(self, name):
        for track in self.tracks:
            if track.get('title') == name:
                return track
        return None

    def get_track_by_id(self, track_id):
        for track in self.tracks:
            if track.get('id') == track_id:
                return track
        return None

    def get_all_artists(self):
        return self.library

    def get_all_artists_info(self):
        artists_info = []
        for artist in self.library:
            artist_info = {
                'artist': artist['artist'],
                'artist_image': artist['artist_image']
            }
            artists_info.append(artist_info)
        return artists_info

    def __str__(self):
        return json.dumps(self.library, indent=4)


if __name__ == '__main__':
    import time

    start = time.perf_counter()
    with open('tracks.json') as f:
        tracks_list = json.load(f)
    library = Library(tracks_list)
    print(library)
    with open('library.json', 'w') as f:    
        json.dump(library.get_library(), f, indent=4)
    finish = time.perf_counter()
    print(f'Finished in {finish - start}s.')
