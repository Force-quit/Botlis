import asyncio
from pytube import YouTube
from pytube import Playlist
from songs import Song, YoutubeSong

class Player:
    """
        Helper class that provides music playing services
    """

    def __init__(self, voice_client, command_channel, loop, guild_id):
        self._guild_id = guild_id
        self._voice_client = voice_client
        self._command_channel = command_channel
        self._loop = loop
        self._queue = []

    async def play(self, url, loading_interaction = None):
        """
        Play a url. 

        loading_interaction is None when the bot is playing a queued song
        """

        song = self.source_factory(url)
        if song is None or song.has_error:
            if loading_interaction is not None:
                await loading_interaction.edit_original_response(content=f"Can't load {url}")
            else:
                await self._command_channel.send(f"Can't load {url}")
            self.song_finished()
            return

        if self._voice_client.is_playing():
            self._queue.append(url)
            # TODO find a way to tell when it's a playlist instead of just one song
            await loading_interaction.edit_original_response(content=f"{song.title} queued!")
            return
        
        source = song.load()
        self._voice_client.play(source, after=self.song_finished)
        
        if loading_interaction is not None:
            await loading_interaction.edit_original_response(content=f"Now playing: {song.title}!")
        else:
            await self._command_channel.send(f"Now playing: {song.title}!")
        
    @property
    def queue(self):
        titles = []

        for url in self._queue:
            song = YouTube(url)
            titles.append(song.title)

        join_str = ", \n".join(titles)
        return join_str
    
    @property
    def has_a_queue(self):
        return len(self._queue) > 0
    
    @property
    def get_queue(self):
        return self._queue

    def song_finished(self, error=None):
        if error is not None:
            print(error)
        elif self.has_a_queue:
            asyncio.run_coroutine_threadsafe(self.play(self._queue.pop(0)), self._loop)
        else:
            asyncio.run_coroutine_threadsafe(self._voice_client.disconnect(), self._loop)

    async def skip(self, ctx):
        if self.has_a_queue:
            await ctx.respond("Skipping...")
            self._voice_client.stop()
        else:
            await ctx.respond("There is no queue my friend")

    #code to add a stop music and disconnect command
    async def stop_and_disconnect(self):
        await self._voice_client.disconnect()

    def source_factory(self, url) -> Song:
        if 'youtube.com/playlist' in url:
            p = Playlist(url)
            song = None

            for i, video in enumerate(p.videos):
                if i == 0:
                    song = YoutubeSong(video.watch_url)
                else:
                    self._queue.append(video.watch_url)
            return song
        elif 'youtube.com/watch' in url or 'youtu.be' in url:
            return YoutubeSong(url)
        
        return None
