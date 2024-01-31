import asyncio
import discord
import os
from enum import IntFlag
from StaticValue import Guild as const
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks

class ProcessStatus(IntFlag):
    NOTHING = 0
    PALWORLD = 1 << 0

class DiscordBot(commands.Bot):

    process_status: ProcessStatus = ProcessStatus.NOTHING
    process_count: int = 0

    def __init__(self, command_prefix: str, intents: discord.Intents, help_command=None):
        super().__init__(command_prefix=command_prefix, intents=intents, help_command=help_command)


    # on_ready前に実行されるイベント 
    async def setup_hook(self) -> None:
        print("セットアップの開始...")
        print("グローバルコマンドを登録します。")
        await self.tree.sync(guild=None)
        print("グローバルコマンド登録完了")
        guilds = const.get_guilds()

        for g in guilds:
            guildName = const.GUILD_SERVER_ID_DICT[g.id]
            print(f"サーバー:{guildName}にコマンドを登録します。")
            try:
                self.tree.copy_global_to(guild=g)
                print(f"サーバー:{guildName}にコマンドを登録しました。")
            except:
                print(f"サーバーID:{guildName}にコマンドを登録できませんでした。")
        print("セットアップ完了")


    # Bot起動時に実行されるイベント
    async def on_ready(self) -> None:
        self.update_status_loop.start()


    # Discord上に表示するゲームのプレイ中ステータスを追加する
    def add_status(self, status: ProcessStatus) -> None:
        self.process_status |= status
        print("add_status: " + status.name)

    # Discord上に表示するゲームのプレイ中ステータスを削除する
    def remove_status(self, status: ProcessStatus) -> None:
        self.process_status &= ~status
        print("remove_status: " + status.name)

    # Discord上に表示するゲームのプレイ中ステータスを即時に更新する
    async def update_status(self) -> None:
        if self.process_status == ProcessStatus.NOTHING:
            self.process_count = 0
            await self.change_presence(activity=discord.Game(name=f"待機中"))
            return
        
        check_bit = (1 << self.process_count)
        if self.process_status.value & check_bit == check_bit:
            await self.change_presence(activity=discord.Game(name=f"{self.process_status.name}"))
            
        self.process_count += 1
        if self.process_count >= len(ProcessStatus):
            self.process_count = 0

    @tasks.loop(seconds=15)
    async def update_status_loop(self):
        await self.update_status()


async def main():
    #Cogフォルダ名
    cog_dir = str("Cogs")            

    # Cogを有効化
    for cog in os.listdir(cog_dir):
        if cog.endswith(".py"):
            print(f"有効化中: {cog}")
            await bot.load_extension(f"{cog_dir}.{cog[:-3]}")
            print(f"有効化完了: {cog}")
            
    # Botを起動
    
    TOKEN = os.getenv("TOKEN")
    print(f"起動します... \nトークン : {TOKEN}")
    await bot.start(TOKEN)


load_dotenv()
ENV = os.getenv("ENV")
load_dotenv(f"env/.env.{ENV}")

# Client生成
intents = discord.Intents.all()
intents.reactions = True
intents.guilds = True
intents.message_content = True
bot = DiscordBot(command_prefix=os.getenv("COMMAND_PREFIX"), intents=intents)

if __name__ == "__main__":    
    asyncio.run(main())