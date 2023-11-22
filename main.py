import discord
from dotenv import dotenv_values

config = dotenv_values(".env")

bot = discord.Bot()

@bot.slash_command()
async def ping(ctx):
    interraction = await ctx.respond("pong!")
    message = await interraction.original_response()
    await message.add_reaction("👌")

if __name__ == "__main__":
    bot.run(config["TOKEN"])