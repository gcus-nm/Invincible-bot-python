import discord
from typing import Final

class Guild:
    # Bot開発用サーバー, メインのサーバー
    GUILD_SERVER_ID_LIST: Final = [951653786307395605, 780434910199808011]
    GUILD_SERVER_ID_DICT: Final = {GUILD_SERVER_ID_LIST[0] : "Bot開発用サーバー", GUILD_SERVER_ID_LIST[1] : "メインのサーバー"}

    @classmethod
    def get_guilds(cls) -> list[discord.abc.Snowflake]:
        list = []
        for i in cls.GUILD_SERVER_ID_LIST:
            list.append(discord.Object(i))
        return list
