from discord.ext import commands

# コグとして用いるクラスを定義。
class SampleCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ping(self, ctx): # 関数名=コマンド名
        '''サンプルの説明''' # helpコマンドに載せる説明を書く
        await ctx.send('pong!')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(SampleCog(bot))
