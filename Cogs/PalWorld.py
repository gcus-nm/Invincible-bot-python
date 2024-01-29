import os
import subprocess
from discord.ext import commands

class PalCog(commands.Cog, group_name='pal'):

    start_process_command = os.getenv("PALWORLD_START_COMMAND")

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('PalWorld.py 起動完了')

    @commands.hybrid_group(name="pal", description="PalWorldサーバーのコマンドです。")
    async def pal(self, ctx:commands.Context):
        pass

    @pal.command(name="start", description="PalWorldサーバーを起動します。")
    async def start(self, ctx:commands.Context):
        print("palWorldサーバーを起動します。")
        subprocess.run(self.start_process_command, shell=True)
        await ctx.send("wake up, palWorld!")

async def setup(bot):
    await bot.add_cog(PalCog(bot))