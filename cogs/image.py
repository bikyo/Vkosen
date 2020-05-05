import discord
from discord.ext import commands
import io
import numpy as np
import cv2

# コグとして用いるクラスを定義。
class ImageCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def color(self, ctx, col): # 関数名=コマンド名
        '''カラーコードから画像を生成''' # helpコマンドに載せる説明を書く
        rgb = []
        try:
            rgb = [int(col[4:6], 16), int(col[2:4], 16), int(col[0:2], 16)]
        except:
            rgb = [0, 0, 0]
        img = np.zeros((200, 300, 3), dtype=np.uint8)
        for i in range(3):
            img[:,:,i] = rgb[i]
        _, buf = cv2.imencode('.png', img)
        buf = io.BytesIO(buf)
        buf.seek(0)
        fl = discord.File(buf, col + '.png')
        await ctx.send(f'rgb = {list(reversed(rgb))}', file=fl)

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(ImageCog(bot))
