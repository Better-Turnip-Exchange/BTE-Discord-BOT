# bot.py
import os

import discord
from server import main as bte_api

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


class CustomClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        if message.author == client.user:
            return
        if "hi" in message.content.lower():
            villager = bte_api.villager()
            villager.villager_id = bte_api.villager_id_generator()
            villager.keywords = ["nmt"]
            villager.price_threshold = 1
            await bte_api.create_villager(villager)
            response = await bte_api.main_driver(villager.villager_id)
            resp_msg = [
                response["islands_visited"][island]["link"]
                for island in response["islands_visited"]
            ]
            resp_msg = "\n".join(resp_msg)
            await message.channel.send(
                "🎈🌴🌴🎈\nHere are your islands {} \n{}\n🎈🌴🌴🎈".format(
                    str(message.author), resp_msg
                )
            )


client = CustomClient()
client.run(TOKEN)
