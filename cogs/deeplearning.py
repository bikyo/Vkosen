from discord.ext import commands
from tensorflow.keras.applications.vgg16 import VGG16, decode_predictions
import cv2
import numpy as np
from pprint import pprint

# コグとして用いるクラスを定義。
class DeepLearningCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.model = VGG16(include_top=True, weights='imagenet', input_shape=(32, 32, 3))

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def category(self, ctx): # 関数名=コマンド名
        '''送られた画像の分類'''
        for attach in ctx.message.attachments:
            if attach.url.endswith(("png", "jpg", "jpeg")):
                data = await attach.read()
                image = cv2.imdecode(np.array(data), 1)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, dsize=(32, 32))
                image = np.expand_dims(image / 255.0, axis=0)
                result = model.predict(image)
                result = decode_predictions(result, top=5)[0]
                await ctx.send(f'{result}')
                
# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(DeepLearningCog(bot))
