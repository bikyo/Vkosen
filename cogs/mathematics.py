from discord.ext import commands
import math

# コグとして用いるクラスを定義。
class MathCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def circle(self, ctx, radius='0'): # 関数名=コマンド名
        '''半径から円の周と面積を求める''' # helpコマンドに載せる説明を書く
        try:
            radius = float(radius)
        except ValueError:
            await ctx.send('数字を入力して下さい')
        else:
            await ctx.send(f'円周：{2.0 * math.pi * radius}\n面積：{math.pi * radius * radius}')

    @commands.command()
    async def sphere(self, ctx, radius='0'):
        '''半径から球の表面積と体積を求める'''
        try:
            radius = float(radius)
        except ValueError:
            await ctx.send('数字を入力して下さい')
        else:
            await ctx.send(f'表面積：{4.0 * math.pi * radius * radius}\n体積　：{4.0 / 3.0 * math.pi * radius * radius * radius}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(MathCog(bot))
