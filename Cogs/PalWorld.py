import os
import subprocess
import socket
import asyncio
from mcrcon import MCRcon
from discord.ext import commands
from discord.ext import tasks

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
        subprocess.run(os.getenv("PALWORLD_START_COMMAND"), shell=True)

        await self.announce_pal_server_start(ctx)
        self.wait_pal_server_wakeup.start(ctx)


    @pal.command(name="stop", description="PalWorldサーバーを停止します。")
    async def stop(self, ctx:commands.Context):
        print("PalWorldサーバーを停止します。")
        await ctx.send("PalWorldサーバーを停止します。")
        await self.send_rcon_command("DoExit")


    @pal.command(name="cmd", description="PalWorldサーバーでコマンドを使用します。")
    async def cmd(self, ctx:commands.Context, *, command:str):
        print(f"コマンド入力:{command}")
        await self.send_rcon_command(command, ctx)


    @tasks.loop(seconds=5)
    async def wait_pal_server_wakeup(self, ctx:commands.Context):
        # 起動まで待つ
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(3)
                    # RCONポートに接続できたら起動完了
                    s.connect((os.getenv("PALWORLD_SERVER_IP_ADDRESS"), int(os.getenv("PALWORLD_RCON_PORT"))))
                    print("PALWORLD RCONポート接続成功")
                    await ctx.send("PalWorldサーバーが起動しました。")
                    break

            except:
                print("PALWORLD RCONポート接続失敗")
                print("再接続開始...")
        
        self.wait_pal_server_wakeup.stop(ctx)
        self.wait_pal_server_stop.start(ctx)       


    @tasks.loop(seconds=5)
    async def wait_pal_server_stop(self, ctx:commands.Context):# 停止まで待つ
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect((os.getenv("PALWORLD_SERVER_IP_ADDRESS"), int(os.getenv("PALWORLD_RCON_PORT"))))
                    
            except:
                await self.announce_pal_server_stop()
                self.wait_pal_server_stop.stop(ctx)
                break        


    async def announce_pal_server_start(self, ctx:commands.Context):        
        await ctx.send("PalWorldサーバーを起動します。")
        print("PalWorldサーバーを起動します。")      
        print(f"接続情報:　IP: {os.getenv('PALWORLD_SERVER_IP_ADDRESS')}, Port: {int(os.getenv('PALWORLD_RCON_PORT'))}")


    async def announce_pal_server_stop(self, ctx:commands.Context):
        await ctx.send("PalWorldサーバーが停止しました。")
        print("PalWorldサーバーが停止しました。")


    async def send_rcon_command(self, command:str, ctx:commands.Context=None):
        with MCRcon(os.getenv("PALWORLD_SERVER_IP_ADDRESS"), os.getenv("PALWORLD_ADMIN_PASSWORD"), int(os.getenv("PALWORLD_RCON_PORT"))) as mcr:
            resp = mcr.command(command)
            print(resp)

            if ctx != None:
                await ctx.send(resp)

            return resp
        

async def setup(bot):
    await bot.add_cog(PalCog(bot))
