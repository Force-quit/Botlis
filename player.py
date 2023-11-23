import asyncio, discord, io
from pytube import YouTube

class Player:
    """
        Helper class that provides music playing services
    """

    def __init__(self, voice_client, command_channel, loop, guild_id, call_when_finished):
        self._guild_id = guild_id
        self._call_when_finished = call_when_finished
        self._voice_client = voice_client
        self._command_channel = command_channel
        self._loop = loop
        self._queue = []
        self._ctx = None
        self._current_title = ""
        self._last_interaction = None
        self._is_skipping = False

    async def play(self, url, loading_interaction = None):
        buffer = io.BytesIO()

        youtube_audio = YouTube(url).streams.get_audio_only()
        youtube_audio.stream_to_buffer(buffer)
        buffer.seek(0)
        self._current_title = youtube_audio.title

        source = discord.FFmpegPCMAudio(buffer, pipe=True)
        if self._voice_client.is_playing():
            self._is_skipping = True
            self._voice_client.stop()
        self._voice_client.play(source, after=self.play_after)
        
        if loading_interaction is not None:
            await loading_interaction.edit_original_response(content=f"Now playing: {self._current_title}!")
        else:
            await self._command_channel.send(f"Now playing: {self._current_title}!")
        

    async def queue(self, ctx, url):
        self._ctx = ctx
        self._queue.append(url)
        youtube_audio = YouTube(url).streams.get_audio_only()
        self._last_interaction = await ctx.respond(f"Track {youtube_audio.title} queued!")

    @property
    def current_title(self):
        return self._current_title
    
    @property
    def has_a_queue(self):
        return len(self._queue) > 0

    def play_after(self, error=None):
        if self._is_skipping:
            self._is_skipping = False
            return

        if error is not None:
            print(error)
        elif self.has_a_queue:
            asyncio.run_coroutine_threadsafe(self.play(self._queue.pop(0)), self._loop)
        else:
            asyncio.run_coroutine_threadsafe(self.disconnect(), self._loop)

    async def disconnect(self):
        self._call_when_finished(self._guild_id)
        await self._voice_client.disconnect()

    async def skip(self, ctx):
        if self.has_a_queue:
            await ctx.respond("Skipping...")
            self.play_after()
        else:
            await ctx.respond("There is no queue my friend")