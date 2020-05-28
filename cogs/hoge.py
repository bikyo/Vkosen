import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import youtube_dl


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


# コグとして用いるクラスを定義。
class VoiceCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.vc = None

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        voice_state = ctx.author.voice
        if (not voice_state) or (not voice_state.channel):
            #もし送信者がどこのチャンネルにも入っていないなら
            await ctx.send('ボイスチャンネルに参加してね')
            return
        channel = voice_state.channel
        self.vc = await channel.connect()
        await ctx.send('Join!')


    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command(aliases=['p'])
    async def play(self, ctx, url=''):
        '''指定された音声ファイルを流します'''
        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            await ctx.send('私はボイスチャンネルに参加していません')
            return
        if self.vc.is_playing():
            self.vc.stop()

        #ffmpeg_audio_source = discord.FFmpegPCMAudio('./music/flowering_night.mp3')
        #voice_client.play(ffmpeg_audio_source)
        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        #voice_client.play(player)
        self.vc.play(player)
        await ctx.send('Play!')

    @commands.command()
    async def pause(self, ctx):
        '''ボイスチャンネルの音楽を止める'''
        if self.vc is not None:
            if(self.vc.is_playing()):
                self.vc.pause()
                await ctx.send('Pause!')

    @commands.command()
    async def resume(self, ctx):
        '''ボイスチャンネルの音楽を止める'''
        if self.vc is not None:
            if(not self.vc.is_playing()):
                self.vc.resume()
                await ctx.send('Resume!')

    @commands.command(aliases=['s'])
    async def stop(self, ctx):
        '''ボイスチャンネルの音楽を止める'''
        if self.vc is not None:
            if(self.vc.is_playing()):
                self.vc.stop()
                await ctx.send('Stop!')

    @commands.command(aliases=['disconnect', 'bye'])
    async def leave(self, ctx):
        '''ボイスチャンネルから切断する'''
        self.voice = None
        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            await ctx.send('Botはこのサーバーのボイスチャンネルに参加していません')
            return
        await voice_client.disconnect()
        self.vc = None


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(VoiceCog(bot))
