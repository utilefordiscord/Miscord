import discord
from discord import opus
from discord.ext import commands
from discord.ext.tasks import loop
import lyricsgenius
import json
import youtube_dl
import asyncio
import time

prefix = "m!"
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

bot.queue_list = []
bot.voiceclient_pause = False
bot.joinvoice_text_channel = None

@bot.event
async def on_ready():
    print("Bot running with:")
    print("User ID: " + str(bot.user.id))
    print("User Name: " + str(bot.user.name))

@bot.command(pass_context=True)
async def ping(ctx):
    em = discord.Embed(title="Response Time: " + str(round(bot.latency,5) * 1000) + " ms", description="", color= 0x2a988d)
    em.set_footer(text="Utile Team 2019")
    await ctx.send(embed=em)

@bot.command(pass_context=True)
async def nitro(ctx):
    em = discord.Embed(title="Are you on the fence about Nitro? Try it. There's many benefits.", color= 0x2a988d)
    em.add_field(name="👉", value="<https://discordapp.com/nitro>")
    em.set_footer(text="Utile Team 2019")
    await ctx.send(embed=em)

@bot.command(pass_context=True)
async def lyrics(ctx, song_name, song_author):
    song = genius.search_song(song_name, song_author)
    lyrics = song.lyrics
    actuallength = len(lyrics)
    messagelength = int(len(lyrics)/1000)

    em = discord.Embed(title="{} by {} was released on {}".format(song.title, song.artist, song.year))
    em.set_thumbnail(url=song.song_art_image_url)
    em.set_footer(text="Utile Team 2019")

    if actuallength < 6000:

        i = 0
        while i < (messagelength + 1):

        #await ctx.send(lyrics[i*2000: (i+1)*2000])
            em.add_field(name="-", value=lyrics[i*1000: (i+1)*1000])
            i+=1
        await ctx.send(embed=em)
    
    else:

        i = 0
        while i < (messagelength + 1):
            await ctx.send(lyrics[i*2000: (i+1)*2000])
            i+=1

@lyrics.error
async def clear_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title="You're missing something!", description="Do {}help {} to see what you're missing!".format(prefix, ctx.command), color= 0x2a988d)
        em.set_footer(text="Utile Team 2019")
        await ctx.send(embed=em)
    
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
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download= stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

bot.voiceclient = None

@bot.command(pass_context=True)
async def play(ctx, *, url):
    
    voice_channel = ctx.message.author.voice.channel

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        bot.voiceclient = await voice_channel.connect(reconnect=True)
        bot.voiceclient.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        
    bot.queue_list.append(url)
    em = discord.Embed(title="Miscord is now playing:", description="{}".format(player.title), color= 0x2a988d)
    em.set_footer(text="Utile Team 2019")
    await ctx.send(embed=em)
    bot.joinvoice_text_channel = ctx.message.channel

@loop(seconds=1)
async def update_queue():
    if bot.voiceclient != None:
        if bot.voiceclient.is_playing() == False:
            if bot.voiceclient_pause == False:

                del bot.queue_list[0]

                if (len(bot.queue_list) == 0):
                    await bot.voiceclient.disconnect()
                    bot.voiceclient = None
                    em = discord.Embed(title="No videos left in queue. Miscord has left the voice channel.", color= 0x2a988d)
                    em.set_footer(text="Utile Team 2019")
                    await bot.joinvoice_text_channel.send(embed=em)
        
                else:
                    player = await YTDLSource.from_url(bot.queue_list[0], loop=bot.loop)
                    bot.voiceclient.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

@bot.command(pass_context=True)
async def stop(ctx):
    await bot.voiceclient.disconnect()
    
    em = discord.Embed(title="Miscord has succesfully disconnected!", color=0x2a988d)
    em.set_footer(text="Utile Team 2019")
    await ctx.send(embed=em)
    bot.voiceclient = None
    bot.queue_list = []

@bot.command(pass_context=True)
async def queue(ctx):
    em = discord.Embed(title="Queue: ", color=0x2a988d)
    for index, song in enumerate(bot.queue_list):
        em.add_field(name="Number {}".format(str(index+1)), value=song)
    
    em.set_footer(text="Utile Team 2019")
    await ctx.send(embed=em)

@bot.command(pass_context=True)
async def add(ctx, *, url):
    bot.queue_list.append(url)
    em = discord.Embed(title="Adding to Queue: ", color=0x2a988d)
    em.add_field(name="URL: ", value="{}".format(url))
    em.set_footer(text="Utile Team 2019")
    await ctx.send(embed=em)

@bot.command(pass_context=True)
async def remove(ctx, *, number:int):
    deleted_url = bot.queue_list[number-1]
    del bot.queue_list[number-1]
    em = discord.Embed(title="Removing from Queue: ", color=0x2a988d)
    em.add_field(name="URL: ", value="{}".format(deleted_url))
    em.set_footer(text="Utile Team 2019")
    await ctx.send(embed=em)

@bot.command(pass_context=True)
async def pause(ctx):
    if bot.voiceclient != None:
        bot.voiceclient_pause = True
        bot.voiceclient.pause()
    else:
        em = discord.Embed(title="Miscord isn't in a voice channel!", color=0x2a988d)
        await ctx.send(embed=em)

@bot.command(pass_context=True)
async def resume(ctx):
    if bot.voiceclient != None:
        bot.voiceclient.resume()
        bot.voiceclient_pause = False
    else:
        em = discord.Embed(title="Miscord isn't in a voice channel!", color=0x2a988d)
        em.set_footer(text="Utile Team 2019")
        await ctx.send(embed=em)

update_queue.start()
bot.run(tokensjson["discord_bot_token"])
