import asyncio
import time

import discord
from HeroInADarkForest import Controller
from HeroInADarkForest import utils
import threading

TOKEN = ""
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages=True
client = discord.Client(intents=intents)
hc = Controller.HeroController()
utils.Utils.client = client
active_game = False


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if (message.author.bot):
        return

    global active_game
    global hc
    content = message.content.lower()
    channel = message.channel

    if not active_game:
        if content == "start":
            print("starting game")
            active_game = True
            hc.display()
            await send(channel)
        return

    # Game runs as normal
    hc.step(content)
    await send(channel)


async def send(channel):
    await channel.send(content=utils.Utils.send_buf)
    # Clear send buf
    utils.Utils.send_buf = ""


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(1)
    loop.create_task(client.start(TOKEN))
    print(2)
    discord_thread = threading.Thread(target=loop.run_forever)
    print(3)
    discord_thread.start()
    print(4)

    time.sleep(5)
    hc = Controller.HeroController()
    print("exiting")
    while True:
        time.sleep(10)
