# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


class CustomClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        if message.author == client.user:
            return
        if "hi" in message.content.lower():
            await message.channel.send("Hello World! 🎈🌴🌴🎈")


client = CustomClient()
client.run(TOKEN)
