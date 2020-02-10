# bot.py
import os
import asyncio
import discord
from dotenv import load_dotenv
import CharacterManager as cm

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

Sol = cm.Character("Sol", 16, 13, 16, 10, 14, 11, 85, "GoLd")
Sol.save_character()
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
    if not client.user.mentioned_in(message):
        return
    if message.author.nick == None:
        await message.channel.send(message.author.mention + " you should set your channel nickname so I can create your character.")
        return

    if("make me" in message.content.lower()):
        msg = message.content[message.content.find("me ")+3:].lower()
        ch = {}
        for word in msg.split():
            ch[word[:word.find("=")]] = word[word.find("=")+1:]
        chname = message.author.nick
        character = cm.Character(chname)
        for stat in cm.STATS:
            try:
                character.set_val(stat, ch[stat.lower()])
            except KeyError:
                continue
            character.set_val('color', ch['color'])
        try:
            character.save_character()
        except cm.CharacterError:
            await message.channel.send(cm.CharacterError.args)
        print("Created: " + chname)

    elif "take this" in message.content.lower():
        character = cm.load_character(message.author.nick)
        msg = message.content[message.content.find("this ") + 5:].lower()
        desc = {}
        for word in msg.split():
            desc[word[:word.find("=")].upper()] = word[word.find("=")+1:]
            if "description" in word:
                break
        desc["DESCRIPTION"] = msg[msg.find("description=") + 12:]
        character.add_item(desc['NAME'].title(), desc)
        character.save_character()




client.run(TOKEN)
