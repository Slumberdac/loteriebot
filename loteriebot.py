"""
Simple loterie bot

Allows opting in and drawing,
with the ability to lock the drawing manually
"""
import os
from random import randint

import discord

intents = discord.Intents.default()
intents.message_content = True  # Can see messages text
intents.members = True  # Can ping members of the server

client = discord.Client(intents=intents)

entries = []
entries_id = []
drawers = []
can_draw = False #pylint: disable=invalid-name


@client.event
async def on_ready():
    """
    Instructions at startup
    """
    print(f"I have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    """
    Instructions called on every message
    """
    global can_draw #pylint: disable=global-statement
    # Here to avoid any risk of infinite loop while developpment,
    # if the recieved message is from yourself, don't do anything
    if message.author == client.user:
        return

    if (
        message.content.casefold() == "!opt-in".casefold()
        and message.author.id not in entries_id
    ):
        entries.append(message.author.name)
        entries_id.append(message.author.id)
        await message.channel.send(f"<@{message.author.id}> has been entered in the draw")
        print(entries)

    if (
        message.content.casefold() == "!draw".casefold()
        and can_draw
        and message.author.id not in drawers
    ):
        user = await client.fetch_user(message.author.id)

        drawers.append(message.author.id)
        index = randint(0, len(entries) - 1)
        while entries_id[index] == message.author.id:
            index = randint(0, len(entries) - 1)

        entries_id.pop(index)

        await user.send(
            f"You have drawn ||**{entries.pop(index)}**||, remember to keep it a secret"
        )
        await message.channel.send(f"<@{message.author.id}> has drawn")


    if (
        message.content.casefold() == "!unlock".casefold()
        and message.author.id == int(os.environ.get("DEV_ID"))
    ):
        can_draw = True
        await message.channel.send("You may now begin drawing")


    if (
        message.content.casefold() == "!lock".casefold()
        and message.author.id == int(os.environ.get("DEV_ID"))
    ):
        can_draw = False
        await message.channel.send("The loterie has been closed, you may not draw anymore")



client.run(os.environ.get("DISCORD_KEY"))
