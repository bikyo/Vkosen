from discord.ext import commands

# コグとして用いるクラスを定義。
class CatCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def neko(self, ctx):
        '''にゃーん'''
        await ctx.send('にゃーん')

    @commands.command()
    async def echo(self, ctx, *args):
        '''オウム返し'''
        args = ' '.join(args)
        await ctx.send(f'{args}')

    @commands.command()
    async def shibuki(self, ctx):
        '''しぶき！しぶき！'''
        await ctx.send('しぶきは神！\nしぶきこそが神！\n唯一神しぶき！！')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(CatCog(bot))
