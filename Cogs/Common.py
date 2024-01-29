from discord.ext import commands
from discord import app_commands
import random

class CommonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Common.py 起動完了')

    @commands.hybrid_command(name="random", description="ランダムな数字を返します。（デフォルトは0~100）")
    @app_commands.describe(max="最大数")
    @app_commands.describe(min="最小数")
    async def random(self, ctx:commands.Context, max:int = 100, min:int = 0):
        random_number = random.randint(min, max)
        await ctx.send(random_number)

async def setup(bot):
    await bot.add_cog(CommonCog(bot))