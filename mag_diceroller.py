# import discord
from discord.ext import commands
from os import environ
from random import randint
import asyncio

die_face = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

TOKEN_VARIABLE_NAME = "DISCORD_TOKEN"
token = ""
try:
    token = environ[TOKEN_VARIABLE_NAME]
except KeyError:
    print("Token variable not set. Quitting.")
    quit()

bot = commands.Bot(command_prefix='>')


def get_roll_text(num):
    roll = [randint(1, 6) for i in range(num)]
    txt = " ".join([die_face[x] for x in roll])
    return roll, txt


def find_repeats(roll):
    repeats = [0 for i in range(6)]
    for die in roll:
        repeats[die - 1] += 1
    return repeats


def get_result(repeats):
    result = 0
    for die in range(5):
        if repeats[die] >= 2:
            result = die + 1

    return result


@bot.command()
async def roll(ctx, num: int):
    if num > 15:
        await ctx.send("Fuck off")
    else:
        roll, text = get_roll_text(num)
        msg = await ctx.send(text)
        for i in range(5):
            await asyncio.sleep(.05)
            roll, text = get_roll_text(num)
            await msg.edit(content=text)

        repeats = find_repeats(roll)
        result = get_result(repeats)
        nudges = repeats[5]
        await msg.edit(content=f"{text}\nResult: {result}  Nudges: {nudges}")


@bot.listen()
async def on_ready():
    # status_message = "Mistborn: Adventure Game (>roll)"
    # await bot.change_presence(activity=discord.Game(name=status_message))
    print("mag_diceroller.py running...")


bot.run(token)
