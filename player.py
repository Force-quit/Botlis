import os, asyncio

# helper class that stores context and other info relevant to the current playback task to be interacted with after playback is finished
class Player:
    def __init__(self, voice_client, loop):
        self.voice_client = voice_client
        self.loop = loop

    def play_after(self, error):
        if error is not None:
            print(error)
        else:
            asyncio.run_coroutine_threadsafe(self.disconnect(), self.loop)

    async def disconnect(self):
        await self.voice_client.disconnect()