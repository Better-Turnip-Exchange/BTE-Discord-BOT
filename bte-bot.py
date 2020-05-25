import os
import discord
from server import main as bte_api

client = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


class CommandHandler:
    """
    CommandHandler taken and mutated from
    https://medium.com/bad-programming/making-a-cool-discord-bot-in-python-3-e6773add3c48

    TODO: Refactor this to the built in commands feature of discord.py
    https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
    """

    def __init__(self, client):
        self.client = client
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    async def command_handler(self, message):
        for command in self.commands:
            if message.content.startswith(command["trigger"]):
                args = message.content.split(" ")
                if args[0] == command["trigger"]:
                    args.pop(0)
                    if command["args_num"] == 0:
                        return await message.channel.send(
                            str(command["function"](message, self.client, args)),
                        )
                        break
                    else:
                        if len(args) >= command["args_num"]:
                            resp = await command["function"](message, self.client, args)
                            return await message.channel.send(
                                message.author.mention + " " + resp,
                            )
                            break
                        else:
                            return await message.channel.send(
                                'command "{}" requires {} argument(s) "{}"'.format(
                                    command["trigger"],
                                    command["args_num"],
                                    ", ".join(command["args_name"]),
                                ),
                            )
                            break
                else:
                    break


ch = CommandHandler(client)


def help_command(message, client, args):
    try:
        count = 1
        coms = "**Commands List**\n"
        for command in ch.commands:
            coms += "{}) {} : {}\n\n".format(count, command["trigger"], command["description"])
            count += 1
        return coms
    except Exception as e:
        print(e)


ch.add_command(
    {
        "trigger": "!help",
        "function": help_command,
        "args_num": 0,
        "args_name": [],
        "description": "Prints a list of all the commands!",
    }
)


async def turnip_search_command(message, client, args):
    try:
        price = int(args[0])
        keywords = args[1:]
        villager = bte_api.villager()
        villager.villager_id = message.author.name
        villager.keywords = keywords
        villager.price_threshold = price
        await bte_api.create_villager(villager)
        response = await bte_api.main_driver(villager.villager_id)
        resp_msg = [
            response["islands_visited"][island]["link"]
            for island in response["islands_visited"]
        ]
        resp_msg = "\n".join(resp_msg)
        if len(resp_msg) > 0:
            return "\n🎈🌴🌴🎈\nHere are your islands\n{}\n🎈🌴🌴🎈".format(resp_msg)
        else:
            return "\n🦝😭😭🦝\nNo islands available\n🦝😭😭🦝\n"
    except Exception as e:
        print(e)
        raise e


ch.add_command(
    {
        "trigger": "!search",
        "function": turnip_search_command,
        "args_num": 2,
        "args_name": ["Price", "Description_Terms"],
        "description": "Searches for turnip prices.\n"
        + "Requires the following arguments {price} {Description_Terms}.\n"
        + "Price: Minimum turnip price.\n"
        + "Description_Terms: Space seperated terms that "
        + "should not appear in the island descriptions.\n"
        + "NOTE: If you don't want to restrict island descriptions put N/A \n"
        + "Example: !search 500 entry fee bells nmt\n"
        + "Example2: !search 200 N/A \n",
    }
)


@client.event
async def on_ready():
    try:
        print(f"{client.user} has connected to Discord!")
        print(client.user.name)
        print(client.user.id)
    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == client.user:
        pass
    else:
        # try to evaluate with the command handler
        try:
            await ch.command_handler(message)
        # message doesn't contain a command trigger
        except TypeError as e:
            raise e
        # generic python error
        except Exception as e:
            print(e)


client.run(TOKEN)
