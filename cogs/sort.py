from discord.ext import commands

# コグとして用いるクラスを定義。
class SortCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def sort(self, ctx, word): # 関数名=コマンド名
        '''文字列をソート'''
        word = sorted(word)
        word = ''.join(word)
        await ctx.send(f'{word}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(SortCog(bot))
