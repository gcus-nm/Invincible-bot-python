import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

class DiscordBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, help_command=None):
        super().__init__(command_prefix=command_prefix, intents=intents, help_command=help_command)
        
    async def setup_hook(self) -> None:
        print("セットアップの開始...")
        # Bot開発用サーバー, メインのサーバー
        guild_ids = [951653786307395605, 780434910199808011]
        await self.tree.sync(guild=None)

        for g in guild_ids:
            try:
                self.tree.copy_global_to(guild=discord.Object(g))
            except discord.errors.Forbidden:
                print(f"サーバーID:{g}に登録できませんでした。")
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
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    print(f"起動します... \nトークン : {TOKEN}")
    await bot.start(TOKEN)

# Client生成
intents = discord.Intents.all()
intents.reactions = True
intents.guilds = True
intents.message_content = True
bot = DiscordBot(command_prefix='/', intents=intents)

if __name__ == "__main__":    
    asyncio.run(main())