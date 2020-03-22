import discord
import random
import time
from mutagen.mp3 import MP3
import pandas as pd
from num2words import num2words
import os

key = os.environ.get('BOOMER_KEY')

def emojifi(message):
    return_message = ""
    for letter in message:
        if letter.isalpha():
            return_message += " :regional_indicator_" + letter + ":"
        elif letter.isspace():
            return_message += "   "
        elif letter.isdigit():
            return_message += ":{}:".format(num2words(letter), lang='en')
    return return_message


def altcaps(message):
    return_message = ""
    for letterPos in range(len(message)):
        if message[letterPos].isalpha():
            letter = message[letterPos]
            rand = random.randint(0, 1)
            if rand:
                return_message += letter.upper()
            else:
                return_message += letter
        else:
            return_message += message[letterPos]
    return return_message



client = discord.Client()


@client.event
async def on_message(message):
    if message.content.startswith("!boomer"):
        if message.content.lower().startswith("!boomer emoji"):
            text = str(message.content).lower().replace("!boomer emoji", "")
            emoji_message = emojifi(text)
            await message.channel.send(emoji_message)
        elif message.content.lower() == "!boomer help":
            embed = discord.Embed(title="Boomer commands", description="List of boomer bot commands")
            embed.add_field(name="!boomer emoji", value="Turns words after initial command into emojis")
            embed.add_field(name="!boomer spamoji", value="Will spam the server with a certain amount of random emojis")
            embed.add_field(name="!boomer altcaps", value="Will return the message with alternating capitals")
            embed.add_field(name="Trump 2020", value="Typing trump 2020 will make the bot patriotic")
            embed.add_field(name="Hillary Clinton", value="Typing hillary clinton will choose one of many rad Hillary themed videos")
            embed.add_field(name="Damn phones", value="Mentioning phones will rile up the boomer army")
            embed.add_field(name="Uh oh", value="Stinky.")
            await message.channel.send(content=None, embed=embed)

        elif message.content.lower() == "!boomer spamoji":
            db = pd.read_csv("emoji_names.csv")
            num = random.randint(0, len(str(message.author)))
            for i in range(num):
                await message.channel.send(db.at[random.randint(0, len(db)), 'name'])

        elif message.content.lower().startswith("!boomer altcaps"):
            text = str(message.content).lower().replace("!boomer altcaps", "")
            await message.channel.send(altcaps(text))

    elif message.content.lower().find("trump 2020") != -1:
        await message.channel.send("Hell yeah brother")

    elif message.content.lower().find("hillary clinton") != -1:
        videos = ["https://www.youtube.com/watch?v=pjS6OdY2dBQ", "https://www.youtube.com/watch?v=WkNL_cfVyWU", "https://www.youtube.com/watch?v=Elvrsn0c1YQ"]
        await message.channel.send(random.choice(videos))

    elif message.content.lower().find("phone") != -1 and str(message.author) != "Boomer#1951":
        await message.channel.send("Fucking millenials always using their phones, back in my day all we had was sodomy.")

    elif message.content.lower().find("uh oh") != -1:
        try:
            channel = message.author.voice.channel
            if channel is not None:
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio('uhoh.mp3'))
                audio = MP3('uhoh.mp3')
                time.sleep(round(audio.info.length))
                await vc.disconnect()
        except AttributeError:
            await message.channel.send("Stinky")

client.run(key)