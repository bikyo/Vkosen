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
        unsei = [('大吉', 20), ('吉', 20), ('中吉', 20), ('小吉', 20), ('末吉', 20), ('凶', 15), ('大凶', 5)]
        num = random.randrange(100)
        un = '平'
        for u in unsei:
            num -= u[1]
            if num < 0:
                un = u[0]
                break
        await ctx.send(f'{ctx.author.display_name}さんの今日の運勢は{un}です！')
    
    @commands.command()
    async def dice(self, ctx, roll='1d6'):
        '''サイコロを投げる'''
        rolls = roll.split('d')
        num = 1
        max_ = 6

        try:
            num = int(rolls[0])
        except:
            pass
        try:
            max_ = int(rolls[1])
        except:
            pass

        result = [str(random.randrange(max_) + 1) for i in range(num)]
        result = ', '.join(result)
        await ctx.send(f'{roll} = {result}')
    
    @commands.command()
    async def amasita(self, ctx):
        '''雨下さんがママか確認'''
        if random.randint(1, 10000) % 10 == 0:
            await ctx.send(f'雨下さんは{ctx.author.display_name}さんのママです。')
        elif random.randint(1, 10000) % 10 == 1:
            await ctx.send(f'雨下さん{ctx.author.display_name}さんのママじゃないので......（冷静）')
        else:
            await ctx.send(f'雨下さんは{ctx.author.display_name}さんのママではありません。')

    @commands.command()
    async def fettuccine(self, ctx):
        '''ランダムでフェットチーネをおすすめ'''
        flavor = ['イタリアングレープ', 'イタリアンピーチ', 'イタリアンレモン', 'カシスオレンジ', 'グレープソーダ', 'コーラ', 'ソーダ']
        num = random.randrange(len(flavor))
        await ctx.send(f'{ctx.author.display_name}さん、フェットチーネグミ{flavor[num]}味がおすすめですよ！')

    @commands.command()
    async def tablet(self, ctx):
        '''ランダムでタブレット菓子をおすすめ'''
        flavor = ['ハイレモン', 'ヨーグレット', 'コーラパンチ', 'カルピスタブレット']
        num = random.randrange(len(flavor))
        await ctx.send(f'{ctx.author.display_name}さん、今日は{flavor[num]}を食べましょう！')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(RandomCog(bot))
