import discord
from discord import opus
from discord.ext import commands
import lyricsgenius
import json
import youtube_dl
import asyncio

prefix = "!"
players = {}

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

        raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))

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

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send("Response Time: " + str(round(bot.latency,2)) + " seconds")

@bot.command(pass_context=True)
async def nitro(ctx):
	await ctx.send("Are you on the fence about Nitro? Try it. There's many benefits.")
	asyncio.sleep(3)
	await ctx.send("👉 <https://discordapp.com/nitro>")

@bot.command(pass_context=True)
async def lyrics(ctx, song_name, song_author):
    #artist = genius.search_artist(song_author, max_songs=1, sort="title")
    song = genius.search_song(song_name, song_author)
    lyrics = song.lyrics
    messagelength = int(len(lyrics)/2000)

    i = 0
    while i < (messagelength + 1):
        await ctx.send(lyrics[i*2000: (i+1)*2000])
        i+=1

@lyrics.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing something! Do {}help {} to see what you're missing!".format(prefix, ctx.command))
    
    raise error

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

bot.voiceclient = None

@bot.command(pass_context=True)
async def play(ctx, *, url):
    
        voice_channel = ctx.message.author.voice.channel

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop)
            bot.voiceclient = await voice_channel.connect(reconnect=True)
            bot.voiceclient.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))

@bot.command(pass_context=True)
async def stop(ctx):
    await bot.voiceclient.disconnect()
    await ctx.send("Miscord has successfully disconnected from your voice channel!")
    bot.voiceclient = None

bot.run(tokensjson["discord_bot_token"])
