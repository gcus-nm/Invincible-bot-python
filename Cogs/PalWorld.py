import os
import asyncio
import subprocess
import socket
from multiprocessing import Process
from mcrcon import MCRcon
from discord.ext import commands

class PalCog(commands.Cog, group_name='pal'):

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
        print("PalWorldサーバーを起動します。")
        p = Process(target=self.start_pal_server, args=("ctx",))
        p.start()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.wait_pal_server_wakeup(ctx))
        

    @pal.command(name="stop", description="PalWorldサーバーを停止します。")
    async def stop(self, ctx:commands.Context):
        print("PalWorldサーバーを停止します。")
        await ctx.send("PalWorldサーバーを停止します。")
        await self.send_rcon_command("stop")

    @pal.command(name="cmd", description="PalWorldサーバーでコマンドを使用します。")
    async def cmd(self, ctx:commands.Context, *, command:str):
        print(f"コマンド入力:{command}")
        await self.send_rcon_command(command, ctx)

    def start_pal_server(self, ctx:commands.Context):
        subprocess.run(os.getenv("PALWORLD_START_COMMAND"), shell=True)

    async def wait_pal_server_wakeup(self, ctx:commands.Context):
        await ctx.send("PalWorldサーバーを起動します。")
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    # RCONポートに接続できたら起動完了
                    s.connect((os.getenv("PALWORLD_SERVER_IP_ADDRESS"), int(os.getenv("PALWORLD_RCON_PORT"))))
                    print("PALWORLD RCONポート接続成功")
                    await ctx.send("PalWorldサーバーが起動しました。")
                    break
            except:
                print("PALWORLD RCONポート接続失敗")
                await asyncio.sleep(1)
                print("再接続開始...")
                pass
        pass

    async def send_rcon_command(self, command:str, ctx:commands.Context=None):
        with MCRcon(os.getenv("PALWORLD_SERVER_IP_ADDRESS"), os.getenv("PALWORLD_ADMIN_PASSWORD"), int(os.getenv("PALWORLD_RCON_PORT"))) as mcr:
            resp = mcr.command(command)
            print(resp)

            if ctx != None:
                await ctx.send(resp)

            return resp

async def setup(bot):
    await bot.add_cog(PalCog(bot))
