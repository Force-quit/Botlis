import os, asyncio

# helper class that stores context and other info relevant to the current playback task to be interacted with after playback is finished
class Player:
    def __init__(self, voice_client, audio_file, loop):
        self.voice_client = voice_client
        self.audio_file = audio_file
        self.loop = loop

    def play_after(self, error):
        if error is not None:
            print(error)
        else:
            asyncio.run_coroutine_threadsafe(self.delete_download(), self.loop)

    async def delete_download(self):
        os.remove(self.audio_file)
        await self.voice_client.disconnect()