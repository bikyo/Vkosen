from discord.ext import commands # Bot Commands Frameworkのインポート
import random


# コグとして用いるクラスを定義。
class RandomCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        random.seed()
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def omikuji(self, ctx):
        '''おみくじを引く'''
        unsei = ['大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶']
        num = random.randrange(len(unsei))
        await ctx.send(f'{ctx.author.name}さんの今日の運勢は{unsei[num]}です！')
    
    @commands.command()
    async def dice(self, ctx, num=6):
        '''サイコロを投げる'''
        try:
            num = int(num)
            if(num <= 0): num = 6
        except:
            num = 6
        await ctx.send(f'dice{num} = {random.randrange(num) + 1}')

    @commands.command()
    async def fettuccine(self, ctx):
        '''おみくじを引く'''
        flavor = ['イタリアングレープ', 'イタリアンピーチ', 'イタリアンレモン', 'カシスオレンジ', 'グレープソーダ', 'コーラ', 'ソーダ']
        num = random.randrange(len(flavor))
        await ctx.send(f'{ctx.author.name}さん、フェットチーネグミ{flavor[num]}味がおすすめですよ！')
    

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(RandomCog(bot))
