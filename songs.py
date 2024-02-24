import discord, io
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

class Song:
    def __init__(self, song_url):
        self._title = ""
        self._url = song_url
        self._has_error = False
    
    @property
    def has_error(self):
        return self._has_error
    
    @property
    def url(self):
        return self._url
    
    def load(self) -> discord.FFmpegPCMAudio:
        raise NotImplementedError("What I said")

    @property
    def title(self):
       raise NotImplementedError("What I said")   
    
class YoutubeSong(Song):
    def __init__(self, song_url):
        Song.__init__(self, song_url)
        self.__youtube_object = None

        try:
            self.__youtube_object = YouTube(song_url, use_oauth=True, allow_oauth_cache=True)
    
            if self.__youtube_object.author == "unknown":
                raise VideoUnavailable(song_url)
            
        except (VideoUnavailable, RegexMatchError):
            self._has_error = True
    
    def load(self) -> discord.FFmpegPCMAudio:
        if self.has_error:
            raise Exception("Tried to load, but this object is invalid")
    
        buffer = io.BytesIO()
        youtube_audio = self.__youtube_object.streams.get_audio_only()
        youtube_audio.stream_to_buffer(buffer)
        buffer.seek(0)

        return discord.FFmpegPCMAudio(buffer, pipe=True, options="-vn")
    
    @property
    def title(self):
        return self.__youtube_object.title