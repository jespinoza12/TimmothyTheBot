### Prerequisites
- [Python 3.6](https://www.python.org/downloads/release/python-368/)
- PIPENV -> `python -m pip install pipenv`
- oauth token & client-id for a Twitch account for your bot

### Installing
1. Open Terminal
3. Install requirements with `pipenv install`
6. Back to the console, `pipenv run python bot.py` to start the bot
7. Type `!test` in the chatroom to test the bot's working


## Bot Interaction
Right now, you can only interact with the bot via the single command, `!test`. You can create similar commands pretty easily, just copy the function and change out the function name decorator arguement...

```python
@bot.command(name='likethis', aliases=['this'])
async def likethis(ctx):
    await ctx.send(f'Asuh, @{ctx.author.name}!')
```

Test is out with `!likethis` in chat! :D

## Events

There are 2 events that are used in the code right now.. `on_ready` and `on_event`.

### on_ready
This executes when the bot comes online, and will print out to the console. 
```python
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')
```

### event_message
This function executes once per event (or message) sent. You can make it handle input from chat that *aren't* necesarily commands, and fun stuff like that.

```python
@bot.event
async def event_message(message):
    print(message.content)
    await bot.handle_commands(message)
```

You can find more info in [TwitchIO's official documentation](https://twitchio.readthedocs.io/en/rewrite/twitchio.html).
