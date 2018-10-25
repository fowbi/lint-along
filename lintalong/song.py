from typing import Dict


class Song:
    def __init__(self, lyrics: str, artist: str, yt_link: str):
        self._lyrics = lyrics
        self._artist = artist
        self._yt_link = yt_link

    @staticmethod
    def new(data: Dict):
        return Song(lyrics=data['lyrics'], artist=data['artist'], yt_link=data['yt_link'])

    @property
    def lyrics(self):
        return self._lyrics

    @property
    def artist(self):
        return self._artist

    @property
    def yt_link(self):
        return self._yt_link
