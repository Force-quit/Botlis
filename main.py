import asyncio, discord
from dotenv import dotenv_values
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
        players[ctx.guild] = Player(voice_client, command_channel, asyncio.get_running_loop(), ctx.guild, player_finished)
    
    try:
        await players[ctx.guild].play(url, interaction)
    except AgeRestrictedError:
        await interaction.edit_original_response(content="This video is age restricted.")
    except Exception as pp:
        await interaction.edit_original_response(content="There seems to be an issue playing this.")

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

#code that checks using the request context if the bot is connected to a Voice Channel in the same server(partial fix to multi-call issue)
def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def player_finished(guild_id):
    del players[guild_id]

if __name__ == "__main__":
    bot.run(config["DEV_TOKEN"])