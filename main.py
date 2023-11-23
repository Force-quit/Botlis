import asyncio, discord
from player import Player
from dotenv import dotenv_values

config = dotenv_values(".env")

bot = discord.Bot()
players = {}

@bot.slash_command(guild_ids=["1177073238346567760"])
async def ping(ctx):
    interraction = await ctx.respond("pong!")
    message = await interraction.original_response()
    await message.add_reaction("👌")

@bot.slash_command()
async def skip(ctx):
    if players.get(ctx.guild):
        await players[ctx.guild].skip(ctx)
    else:
        interraction = await ctx.respond("No music is playing wa de hell boi")
        message = await interraction.original_response()
        await message.add_reaction("🤨")

@bot.slash_command()
async def play(ctx, url):
    if is_connected(ctx):
        await players[ctx.guild].queue(ctx, url)
        return 
    
    interaction = await ctx.respond("Loading this bitch up")
    voice_channel = ctx.author.voice.channel
    command_channel = ctx.channel
    
    #connect to the VC
    voice_client = await voice_channel.connect()
    
    #generate the Player instance that will handle cleanup with existing request data
    players[ctx.guild] = Player(voice_client, command_channel, asyncio.get_running_loop(), ctx.guild, player_finished)
    await players[ctx.guild].play(url, interaction)

#code that checks using the request context if the bot is connected to a Voice Channel in the same server(partial fix to multi-call issue)
def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def player_finished(guild_id):
    del players[guild_id]

if __name__ == "__main__":
    bot.run(config["TOKEN"])