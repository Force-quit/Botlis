import asyncio, discord, io
from player import Player
from dotenv import dotenv_values
from pytube import YouTube

config = dotenv_values(".env")

bot = discord.Bot()

@bot.slash_command(guild_ids=["1177073238346567760"])
async def ping(ctx):
    interraction = await ctx.respond("pong!")
    message = await interraction.original_response()
    await message.add_reaction("👌")

@bot.slash_command()
async def play(ctx, url):
    if not is_connected(ctx):
        #interact with the request to enable 15 minute interaction window
        interaction = await ctx.respond("Loading this bitch up")
        
        #gather the data for the request
        channel = ctx.author.voice.channel
        buffer = io.BytesIO()
        youtube_audio = YouTube(url).streams.filter(only_audio=True).first()
        youtube_audio.stream_to_buffer(buffer)
        voice_client = await channel.connect()
        buffer.seek(0)
        #generate the Player instance that will handle cleanup with existing request data
        player = Player(voice_client, asyncio.get_running_loop())
        
        #generate the audio and play it
        source = discord.FFmpegPCMAudio(buffer, pipe=True)
        voice_client.play(source, after=player.play_after)# after is the callback to our player cleanup code
        
        #modify the original interaction message to show we are live and also refresh the interaction window
        await interaction.edit_original_response(content=f"You're playing {youtube_audio.title}")
    else:
        interaction = await ctx.respond("Sorry, I'm already playing a song somewhere.")

#code that checks using the request context if the bot is connected to a Voice Channel in the same server(partial fix to multi-call issue)
def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

if __name__ == "__main__":
    bot.run(config["TOKEN"])