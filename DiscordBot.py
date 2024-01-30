import asyncio
import discord
import os
from StaticValue import Guild as const
from dotenv import load_dotenv
from discord.ext import commands

class DiscordBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, help_command=None):
        super().__init__(command_prefix=command_prefix, intents=intents, help_command=help_command)
        
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