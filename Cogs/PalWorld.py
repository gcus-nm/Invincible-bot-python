import os
import subprocess
import socket
import threading
from mcrcon import MCRcon
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from DiscordBot import ProcessStatus

class PalCog(commands.Cog, group_name='pal'):

    startCtx:commands.Context = None

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

        if self.get_is_pal_server_running() == True:
            print("PalWorldサーバーが既に起動しています。")
            await ctx.send("PalWorldサーバーが既に起動しています。")
            self.bot.add_status(ProcessStatus.PALWORLD)
            return
        
        thread = threading.Thread(target=self.start_pal_server)
        thread.start()

        self.startCtx = ctx

        print("PalWorldサーバーを起動します。")      
        print(f"接続情報:　IP: {os.getenv('PALWORLD_SERVER_IP_ADDRESS')}, Port: {int(os.getenv('PALWORLD_RCON_PORT'))}")
        await self.startCtx.send("PalWorldサーバーを起動します。")

        if self.wait_pal_server_wakeup.is_running == True:
            self.wait_pal_server_wakeup.stop()

        self.wait_pal_server_wakeup.start()


    @pal.command(name="stop", description="PalWorldサーバーを停止します。")
    @app_commands.rename(shutdown_time="シャットダウン時間")
    @app_commands.rename(shutdown_message="メッセージ")
    @app_commands.describe(shutdown_time="停止までの時間（秒）")
    @app_commands.describe(shutdown_message="シャットダウン開始時にサーバーで全員に通知するメッセージ")
    async def stop(self, ctx:commands.Context, shutdown_time:int = 0, shutdown_message:str = None):

        if self.get_is_pal_server_running() == False:
            print("PalWorldサーバーに接続出来ません。")
            await ctx.send("PalWorldサーバーに接続出来ません。")
            return
        
        isDoExit = shutdown_time <= 0
        stop_default_message = "PalWorldサーバーを停止します。"
        message = f"{shutdown_time}秒後に" + stop_default_message + f"\n{shutdown_message}" if isDoExit == False else stop_default_message
        cmd = f"Shutdown {shutdown_time} {shutdown_message}" if isDoExit == False else "DoExit"

        print(message)
        await ctx.send(message)
        await self.send_rcon_command(cmd)


    @pal.command(name="player", description="PalWorldサーバーに接続しているプレイヤーを確認します。")
    async def player(self, ctx:commands.Context):
        
        if self.get_is_pal_server_running() == False:
            print("PalWorldサーバーに接続出来ません。")
            await ctx.send("PalWorldサーバーに接続出来ません。")
            return

        resp = await self.send_rcon_command("ShowPlayers")
        await ctx.send(f"プレイヤー一覧情報\n{resp}")
        

    @pal.command(name="status", description="PalWorldサーバーの状態を確認します。")
    async def status(self, ctx:commands.Context):
        if self.get_is_pal_server_running() == False:
            print("PalWorldサーバーに接続出来ません。")
            await ctx.send("PalWorldサーバーに接続出来ません。")
            return

        await ctx.send("PalWorldサーバーに接続出来ました。")


    @pal.command(name="cmd", description="PalWorldサーバーでコマンドを使用します。")
    async def cmd(self, ctx:commands.Context, *, command:str):
        print(f"コマンド入力:{command}")
        await self.send_rcon_command(command, ctx)


    @tasks.loop(seconds=5)
    async def wait_pal_server_wakeup(self):
        # 起動まで待つ
        if self.get_is_pal_server_running() == False:
            print("PALWORLD RCONポート接続待機中")
            return
        
        print("PALWORLD RCONポート接続成功")
        await self.startCtx.send("PalWorldサーバーが起動しました。")
        self.bot.add_status(ProcessStatus.PALWORLD)
        await self.bot.update_status()

        if self.wait_pal_server_stop.is_running == True:
            self.wait_pal_server_stop.stop()

        self.wait_pal_server_stop.start()
        self.wait_pal_server_wakeup.stop()


    @tasks.loop(seconds=5)
    async def wait_pal_server_stop(self):
        # 停止まで待つ
        if self.get_is_pal_server_running() == True:
            print("PALWORLD RCONポート接続中")
            return
                
        print("PalWorldサーバーが停止しました。")
        await self.startCtx.send("PalWorldサーバーが停止しました。")
        self.bot.remove_status(ProcessStatus.PALWORLD)
        await self.bot.update_status()
        self.wait_pal_server_stop.stop()


    def start_pal_server(self):
        subprocess.run(os.getenv("PALWORLD_START_COMMAND"), shell=True)
        
        
    def get_is_pal_server_running(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((os.getenv("PALWORLD_SERVER_IP_ADDRESS"), int(os.getenv("PALWORLD_RCON_PORT"))))
                return True
        except:
            return False        


    async def send_rcon_command(self, command:str, ctx:commands.Context=None):
        with MCRcon(os.getenv("PALWORLD_SERVER_IP_ADDRESS"), os.getenv("PALWORLD_ADMIN_PASSWORD"), int(os.getenv("PALWORLD_RCON_PORT"))) as mcr:
            resp = mcr.command(command)
            print(resp)

            if ctx != None:
                await ctx.send(f"コマンド結果：{resp}")

            return resp
        

async def setup(bot):
    await bot.add_cog(PalCog(bot))
