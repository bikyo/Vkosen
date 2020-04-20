from discord.ext import commands # Bot Commands Frameworkのインポート
import random

# コグとして用いるクラスを定義。
class GatyaCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        random.seed()
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def gatya(self, ctx):
        '''V高専がチャを回す'''
        rarity = ['N  ', 'R  ', 'SR', 'UR']
        gat = []
        gat.append(['秋風御礼', '浅浪沫', '雨下青猫', 'あんかるむ', '絵村千咲', '音無りんこ', '神爪しお', '神爪緑', '夏眠', '如月璃音', '北川茜', '西行響希', '空辺飛狐', '敷島佑斗', '辞典', '霜暮黒夢', '春眠', '単位パン', '千早旅兎', '九十九零', '鉄城大和', '冬眠', '泡影布目', 'モブヶ崎モブ夫', '山吹勇麻', '雪野冬磨'])
        gat.append(['調整中'])
        gat.append(['調整中'])
        gat.append(['chokudai', '七瀬真冬'])
        string = 'ガチャ結果\n'
        for i in range(10):
            rare = random.randrange(1000)
            if(rare < 600): rare = 0
            elif(rare < 900): rare = 1
            elif(rare < 995): rare = 2
            else: rare = 3
            if i == 10 - 1:
                if rare < 2: rare = 2
            res = random.randrange(len(gat[rare]))
            string += f'{rarity[rare]}：{gat[rare][res]}\n'
        await ctx.send(string)

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(GatyaCog(bot))
