import discord
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
    interaction = await ctx.respond("Loading this bitch up")
    channel = ctx.author.voice.channel
    youtube_audio = YouTube(url).streams.filter(only_audio=True).first()
    audio_file = youtube_audio.download(output_path="downloads")
    voice_client = await channel.connect()
    source = discord.FFmpegPCMAudio(audio_file)
    voice_client.play(source)
    await interaction.edit_original_response(content=f"You're playing {youtube_audio.title}")
    
if __name__ == "__main__":
    bot.run(config["TOKEN"])