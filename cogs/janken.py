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
        rotehands = ['パー', 'グー', 'チョキ', 'パー', 'グー']
        if not hand in rotehands:
            await ctx.send('じゃんけんの手を出してください')
            return

        num = random.randrange(999) % 3 - 1
        string = 'Vbotの手 : '
        for i in range(1, 4):
            if hand == rotehands[i]:
                string += rotehands[i + num] + '\n'

        if num == -1:
            string += 'Vbotの勝ちだよ'
        if num == 0:
            string += 'アイコだよ'
        if num == 1:
            string += f'{ctx.author.name}さんの勝ち！'
        await ctx.send(f'{string}')
    

    @commands.command()
    async def honda(self, ctx, hand):
        '''じゃんけん'''
        num = random.randrange(1000)
        string = 'Vbotの手 : '
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

        if num < 10:
            string += '\nやるやん！\n明日は俺にリベンジさせて。\nでは、どうぞ。'
        else:
            string += '\n俺の勝ち！\n'
            if hand == 'グー':
                string += '負けは次につながるチャンスです。\nネバーギブアップ！'
            if hand == 'チョキ':
                string += 'たかがじゃんけん、そう思ってないですか？\nそれやったら明日も俺が勝ちますよ。'
            if hand == 'パー':
                string += 'なんで負けたか、明日まで考えといてください。\nそしたら何かが見えてくるはずです。'
            string += '\nほな、いただきます。'
        await ctx.send(f'{string}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(JankenCog(bot))
