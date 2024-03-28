import asyncio, discord, io
from dotenv import dotenv_values
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from player import Player

config = dotenv_values(".env")

bot = discord.Bot()
players = {}

@bot.slash_command(guild_ids=["1177073238346567760"], description="Pings the bot to see if it's alive")
async def ping(ctx):
    interraction = await ctx.respond("pong!")
    message = await interraction.original_response()
    await message.add_reaction("👌")

@bot.slash_command(description="Skips to the next track in the queue")
async def skip(ctx):
    if players.get(ctx.guild):
        await players[ctx.guild].skip(ctx)
    else:
        interraction = await ctx.respond("No music is playing wa de hell boi")
        message = await interraction.original_response()
        await message.add_reaction("🤨")

@bot.slash_command(description="Play music by providing a link. Also works for playlist links.")
async def play(ctx, url):
    interaction = await ctx.respond("Loading this bitch up")

    if not players.get(ctx.guild):
        voice_channel = ctx.author.voice.channel
        command_channel = ctx.channel
        voice_client = await voice_channel.connect()
        players[ctx.guild] = Player(voice_client, command_channel, asyncio.get_running_loop(), ctx.guild)
    
    try:
        await players[ctx.guild].play(url, interaction)
    except AgeRestrictedError:
        await interaction.edit_original_response(content="This video is age restricted.")
    except Exception as pp:
        await interaction.edit_original_response(content=f"There seems to be an issue playing this. {pp}")

@bot.slash_command(description="Show the current queue.")
async def queue(ctx):
    if is_connected(ctx):
        if players[ctx.guild].has_a_queue:
            message = await ctx.respond("Loading...")
            await message.edit_original_response(content=players[ctx.guild].queue)
        else:
            await ctx.respond("No queue")
    else:
        await ctx.respond("Not connected here")

#Code to implement bot stop music command
@bot.slash_command(description="Stops the music and disconnects the bot")
async def stop(ctx):
    if players.get(ctx.guild):
        await players[ctx.guild].stop_and_disconnect()
        await ctx.respond("Stopped and disconnected.")
    else:
        await ctx.respond("No active player found.")

# create Slash Command group with bot.create_group
mencaliss = bot.create_group("mencaliss", "???")

@mencaliss.command()
async def vc(ctx):
    await play(ctx, "https://www.youtube.com/watch?v=FG-Ldd2YDPY")

@mencaliss.command()
async def vid(ctx):
    interaction = await ctx.respond("Loading...")
    video = YouTube("https://www.youtube.com/watch?v=FG-Ldd2YDPY")
    video_buffer = io.BytesIO()
    video_stream = video.streams.get_highest_resolution()
    video_stream.stream_to_buffer(video_buffer)
    video_buffer.seek(0)
    video_file = discord.File(video_buffer, filename="video.mp4")
    await interaction.edit_original_response(content="", file=video_file)

#code that checks using the request context if the bot is connected to a Voice Channel in the same server(partial fix to multi-call issue)
def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user and after.channel is None:
        del players[before.channel.guild]

if __name__ == "__main__":
    bot.run(config["DEV_TOKEN"])