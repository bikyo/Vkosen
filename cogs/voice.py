import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import youtube_dl
import asyncio


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
        self.url_queue = []

    def play_after(self, e=None):
        fut = asyncio.run_coroutine_threadsafe(self.play_queue(), self.bot.loop)
        try:
            fut.result()
        except:# exceptions as error:
            print('error')

    async def play_queue(self):
        if self.url_queue:
            player = await YTDLSource.from_url(self.url_queue[0], loop=self.bot.loop)
            #await ctx.send(f'Play {self.url_queue[0]}')
            del self.url_queue[0]
            self.vc.play(player, after=self.play_after)

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        '''ボイスチャンネルへ参加'''
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
        '''指定された音声ファイルを流す'''
        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            await ctx.send('私はボイスチャンネルに参加していません')
            return
        if self.vc.is_playing():
            #self.vc.stop()
            self.url_queue.append(url)
            url_str = 'Queue'
            for i in range(len(self.url_queue)):
                url_str += '\n' + str(i+1) + '：' + self.url_queue[i]
            await ctx.send(f'{url_str}')
            return

        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        self.vc.play(player, after=self.play_after)
        #self.vc.play(player)
        await ctx.send('Play!')

    @commands.command()
    async def pause(self, ctx):
        '''再生中の音楽を一時停止'''
        if self.vc is not None:
            if(self.vc.is_playing()):
                self.vc.pause()
                await ctx.send('Pause!')

    @commands.command()
    async def resume(self, ctx):
        '''一時停止中の音楽を再開'''
        if self.vc is not None:
            if(not self.vc.is_playing()):
                self.vc.resume()
                await ctx.send('Resume!')

    @commands.command(aliases=['st'])
    async def stop(self, ctx):
        '''ボイスチャンネルの音楽を止める'''
        if self.vc is not None:
            if(self.vc.is_playing()):
                self.vc.stop()
                await ctx.send('Stop!')

    @commands.command(aliases=['sk'])
    async def skip(self, ctx):
        '''現在の曲をスキップする'''
        if self.vc is not None:
            if self.url_queue:
                if(self.vc.is_playing()):
                    self.vc.stop()
                self.play_after()
            
    
    @commands.command()
    async def clear(self, ctx):
        '''キューを空にする'''
        self.url_queue = []
        await ctx.send('Clear Queue!')

    @commands.command(aliases=['del'])
    async def delete(self, ctx, num):
        '''指定した要素を削除する(1から)'''
        try:
            num = int(num)
            del self.url_queue[num]
        except:
            await ctx.send('有効な整数を渡してください')
        else:
            await ctx.send('Deleted!')

    @commands.command(aliases=['disconnect', 'bye'])
    async def leave(self, ctx):
        '''ボイスチャンネルから切断する'''
        self.voice = None
        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            await ctx.send('Botはこのサーバーのボイスチャンネルに参加していません')
            return
        self.url_queue = []
        await voice_client.disconnect()
        self.vc = None
        await ctx.send('Bye!')


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(VoiceCog(bot))
