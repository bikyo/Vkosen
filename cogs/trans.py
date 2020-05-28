from discord.ext import commands
from googletrans import Translator

# コグとして用いるクラスを定義。
class TransCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def trans(self, ctx, word, src, dst): # 関数名=コマンド名
        '''翻訳[文、翻訳元言語、翻訳後言語]'''
        await ctx.send(f'{Translator().translate(word, src=src, dest=dst).text}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(TransCog(bot))
