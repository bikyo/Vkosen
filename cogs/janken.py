from discord.ext import commands
import random


# コグとして用いるクラスを定義。
class JankenCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def janken(self, ctx, hand):
        '''じゃんけん'''
        num = random.randrange(1000) % 2
        string = '望鳴の手 : '
        if hand == 'グー':
            string += 'チョキ' if num == 0 else 'パー'
        elif hand == 'チョキ':
            string += 'パー' if num == 0 else 'グー'
        elif hand == 'パー':
            string += 'グー' if num == 0 else 'チョキ'
        else:
            string = 'じゃんけんの手を出してください'
            await ctx.send(f'{string}')
            return
        string += '\n'
        string += f'{ctx.author.name}さんの勝ち！' if num == 0 else '望鳴の勝ちだよ'
        await ctx.send(f'{string}')
    

    @commands.command()
    async def honda(self, ctx, hand):
        '''じゃんけん'''
        num = random.randrange(1000)
        string = '望鳴の手 : '
        if hand == 'グー':
            string += 'チョキ' if num < 10 else 'パー'
        elif hand == 'チョキ':
            string += 'パー' if num < 10 else 'グー'
        elif hand == 'パー':
            string += 'グー' if num < 10 else 'チョキ'
        else:
            string = 'じゃんけんの手を出してください'
            await ctx.send(f'{string}')
            return
        string += '\n'
        string += f'{ctx.author.name}さんの勝ち！' if num == 0 else '俺の勝ち！'
        await ctx.send(f'{string}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(JankenCog(bot))
