import asyncio, discord
from dotenv import dotenv_values
from player import Player
from pytube import YouTube


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
    if is_connected(ctx):
        await players[ctx.guild].queue(ctx, url)
        return 
    
    interaction = await ctx.respond("Loading this bitch up")
    try:
        voice_channel = ctx.author.voice.channel
        command_channel = ctx.channel

        #connect to the VC
        voice_client = await voice_channel.connect()

        #generate the Player instance that will handle cleanup with existing request data
        players[ctx.guild] = Player(voice_client, command_channel, asyncio.get_running_loop(), ctx.guild, player_finished)
        await players[ctx.guild].play(url, interaction)
    except:
        await interaction.edit_original_response(content="There seems to be an issue connecting to the server. Are you in a voice channel?")

@bot.slash_command(description="Show the current queue.")
async def queue(ctx):
    if is_connected(ctx):
        if players[ctx.guild].has_a_queue:
            interaction = await ctx.respond("Loading...")
            titles = []
            for url in players[ctx.guild].get_queue:
                youtube_audio = YouTube(url).streams.get_audio_only()
                titles.append(youtube_audio.title)
            join_str = ", \n".join(titles)
            await interaction.edit_original_response(content=f"Current queue: {join_str}")
        else:
            await ctx.respond("No queue")
    else:
        await ctx.respond("Not connected here")

#code that checks using the request context if the bot is connected to a Voice Channel in the same server(partial fix to multi-call issue)
def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def player_finished(guild_id):
    del players[guild_id]

if __name__ == "__main__":
    bot.run(config["DEV_TOKEN"])