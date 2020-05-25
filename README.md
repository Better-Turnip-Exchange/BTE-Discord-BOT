# BTE-BOT

A command driven discord bot that helps villagers find islands to visit and sell
turnips.

## Usage

1. `pip install -r requirements`
2. `python bte-bot.py`

### Usage TODO

- Makefile
- Dockerize bot

## Documentation

### Class: `CommandHandler`

Create a `CommandHandler` object by instancing the `ch = CommandHandler(client)` class.

```python
client = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
# ...
ch = CommandHandler(client)
```

### `ch.add_command`

Create a custom command for the `CommandHandler` object to call.

Example custom command

```python
def hello_world_command(message, client, args):
    try:
        print("Hello World!")
    except Exception as e:
        raise e
```

Add the custom command using `add_command`

```python
ch.add_command(
    {
        "trigger": "!hello",
        "function": hello_world_command,
        "args_num": 0,
        "args_name": [],
        "description": "Prints hello world!",
    }
)
```

The `CommandHandler` object's `commands` attribute (`self.commands = []`) is an
array of dictionaries with the following keys.

```python
    # "trigger": The Trigger string for the bot to listen to from the user
    #           [2:13 AM] Zagan: !hello
    #           [2:13 AM] BOT: Hello World!
    # "function": The function the command handler should call when command is issued
    # "args_num": How many arguments the custom command expects?
    #             def hello_world_command(message, client, args):
    #               ...
    #             args is a list of strings given via the chat
    #             ie any strings given after the trigger string
    # "args_name": What arguments we expect this custom command function needs
    # description": What does custom command function do?
```

### `async def command_handler(self, message)`

The main "handler" logic the break up user message to "handle" the different parts
of the message.

Here's the high level logic

```text
 for each command_dict in `commands` list attribute
    - if the message begins with the trigger string
       ex) "!help"
        - Split string into string arr called args
        - if the first elem in the args list is trigger
          - pop the first arg off the list
          - if the args number is 0
            - call the command in that command_dict's function key
          - else
            - if the args given is equal or more command_dict's function key
              - call the command in that command_dict's function key
            - else if the args given less command_dict's function key
              - Tell the user that they're missing arguments needed for the function they want to call
```

#### Events

Connecting the bot to discord ready to accept commands

```python
@client.event
async def on_ready():
    try:
        print(f"{client.user} has connected to Discord!")
        print(client.user.name)
        print(client.user.id)
    except Exception as e:
        print(e)
```

Accept messages from users

```python
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
```