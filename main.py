import asyncio, discord
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
        youtube_audio = YouTube(url).streams.filter(only_audio=True).first()
        audio_file = youtube_audio.download(output_path="downloads")
        voice_client = await channel.connect()
        
        #generate the Player instance that will handle cleanup with existing request data
        player = Player(voice_client, audio_file, asyncio.get_running_loop())
        
        #generate the audio and play it
        source = discord.FFmpegPCMAudio(audio_file)
        voice_client.play(source, after=player.play_after)# after is the callback to our player cleanup code
        
        #modify the original interaction message to show we are live and also refresh the interaction window
        await interaction.edit_original_response(content=f"You're playing {youtube_audio.title}")
    else:
        interaction = await ctx.respond("Sorry, I'm already playing a song somewhere.")

#code that checks using the request context if the bot is connected to a Voice Channel in the same server(partial fix to multi-call issue)
def is_connected(ctx):
    guilds = discord.utils.get(ctx.bot.guilds)
    for guild in guilds:
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=guild)
        if voice_client and voice_client.is_connected():
            return True
    return False

if __name__ == "__main__":
    bot.run(config["TOKEN"])