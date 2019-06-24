import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import lyricsgenius
import json

prefix = "!"

##If you're going to try running this, make sure you create tokens.json with a genius_login_token and discord_bot_token for this to work
with open('hackweek/tokens.json') as f:
	tokensjson = json.load(f)

bot = commands.Bot(command_prefix= prefix)
genius = lyricsgenius.Genius(str(tokensjson["genius_login_token"]))

@bot.event
async def on_ready():
    print("Bot running with:")
    print("User ID: " + str(bot.user.id))
    print("User Name: " + str(bot.user.name))

#@bot.event
#async def on_message(message):
#    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Response Time: " + str(round(bot.latency,2)) + " seconds")

@bot.command()
async def searchsong(ctx, song_name, song_author):
    #artist = genius.search_artist(song_author, max_songs=1, sort="title")
    song = genius.search_song(song_name, song_author)
    lyrics = song.lyrics
    messagelength = int(len(lyrics)/2000)

    i = 0
    while i < (messagelength + 1):
        await ctx.send(lyrics[i*2000: (i+1)*2000])
        i+=1


@searchsong.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing something! Do {}help {} to see what you're missing!".format(prefix, ctx.command))
    
    raise error

bot.run(tokensjson["discord_bot_token"])