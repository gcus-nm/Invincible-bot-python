import discord
from discord.ext import commands
from discord import app_commands
import random

class CommonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Common.py 起動完了')

    @app_commands.command(name="random", description="ランダムな数字を返します。（デフォルトは0~100）")
    @discord.app_commands.describe(max="最大数")
    @discord.app_commands.describe(min="最小数")
    async def random(self, interaction: discord.Interaction, max:int = 100, min:int = 0):
        random_number = random.randint(min, max)
        await interaction.response.send_message(random_number)

async def setup(bot):
    await bot.add_cog(CommonCog(bot))