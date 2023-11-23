import discord
import os
from dotenv import dotenv_values
from pytube import YouTube

config = dotenv_values(".env")

bot = discord.Bot()

@bot.slash_command()
async def ping(ctx):
    interraction = await ctx.respond("pong!")
    message = await interraction.original_response()
    await message.add_reaction("👌")

@bot.slash_command()
async def play(ctx, url):
    if not is_connected(ctx):
        interaction = await ctx.respond("Loading this bitch up")
        channel = ctx.author.voice.channel
        youtube_audio = YouTube(url).streams.filter(only_audio=True).first()
        audio_file = youtube_audio.download(output_path="downloads")
        voice_client = await channel.connect()
        source = discord.FFmpegPCMAudio(audio_file)
        voice_client.play(source, lambda error: delete_download(audio_file))
        await interaction.edit_original_response(content=f"You're playing {youtube_audio.title}")
    else:
        interaction = await ctx.respond("Sorry, I'm already playing a song somewhere.")

#should delete the downloaded audio once we're done playing
def delete_download(audio_file):
    os.remove(f"downloads/{audio_file}")

#code that checks using the request context if the bot is connected to a Voice Channel in the same server(partial fix to multi-call issue)
def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

if __name__ == "__main__":
    bot.run(config["TOKEN"])