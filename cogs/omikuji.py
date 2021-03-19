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
        unsei = [('大吉', 10), ('吉', 25), ('中吉', 15), ('小吉', 15), ('末吉', 15), ('凶', 15), ('大凶', 5)]
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

        if len(rolls) >= 2:
            num = int(rolls[0])
            max_ = int(rolls[1])
        elif len(rolls) == 1:
            if roll[0] == 'd':
                max_ = int(rolls[0])
            elif roll[-1] == 'd':
                num = int(rolls[0])

        result = [random.randrange(max_) + 1 for i in range(len(num))]
        result = ', '.join(result)
        await ctx.send(f'{roll} = {result}')

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
