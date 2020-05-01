from discord.ext import commands
import sympy as sym
from sympy import *
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

    @commands.command()
    async def diff(self, ctx, y='0', n='1'):
        '''関数をxで微分する'''
        x = sym.symbols('x')
        try:
            y = eval(y)
            n = abs(int(n))
        except:
            await ctx.send('Pythonのフォーマットに対応した変数はxのみの数式を入力してください')
        else:
            y = sym.diff(y, x, n)
            prime = ['\'' for i in range(n)]
            prime = ''.join(prime)
            await ctx.send(f'y{prime} = {y}')

    @commands.command()
    async def intg(self, ctx, y='0', a='0', b='0'):
        '''関数をxで積分する'''
        x = sym.symbols('x')
        try:
            y = eval(y)
            a = int(a)
            b = int(b)
        except:
            await ctx.send('Pythonのフォーマットに対応した変数はxのみの数式を入力してください')
        else:
            if a == b:
                y = sym.integrate(y, x)
                await ctx.send(f'∫ydx = {y}')
            else:
                y = sym.integrate(y, (x, a, b))
                await ctx.send(f'∫[{a}:{b}]ydx = {y}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(MathCog(bot))
