from discord.ext import commands # Bot Commands Frameworkのインポート

# コグとして用いるクラスを定義。
class GreetCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def hello(self, ctx):
        '''出会いのあいさつをする'''
        await ctx.send(f'どうも、{ctx.author.display_name}さん!')

    @commands.command()
    async def goodbye(self, ctx):
        '''別れの挨拶をする'''
        await ctx.send(f'じゃあね、{ctx.author.display_name}さん!')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(GreetCog(bot))
