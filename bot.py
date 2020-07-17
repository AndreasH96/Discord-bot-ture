import discord
import platform
import base64
import datetime
from discord.ext import commands
import sys
import asyncio
from itertools import cycle
import json

encryptedKeys = {"live": "\r\x03I<?\x12\x01\t\x1e2)sk2\\\r&7'n5&S\x18\\91#X\x1e\x1f x\x14%Y/\x0eDo<jG+\x05a6\x07\x08\x08Yz\x08\x00w1\x08\x02\x0c\x0c\x03\x01u\x0c^#4@=\r/n!\x1a<\x157[7\x0e\x04x",
                "local": "\r\x03I<?\x02\x05N\x1e>\x07ro5\x01\n&6\x05n6\x18[{d95=k4\x0f x\x14%Y(n;7<jG\x0c5p.\x17?&{C;\x17{D\x00ezN\x1e<\x1fvP5/}$k\r}\x1a\x05\x1a\x1c7^\x11 \x04x"}

IDs = {"serverID":467039975276281856, "ture-har-ordet":729990369525235772, "vmguld-i-skitsnack":467039975276281858}

isLocal = True
botVersion = 0.00

with open('messages.json', encoding='utf-8') as json_data:
    messages = json.load(json_data)
# ------------------------------- Encryption -------------------------------

def xor_strings(string, theKey):
    """xor two strings together"""
    if isinstance(string, str):
        # Text strings contain single characters
        return b"".join(chr(ord(a) ^ ord(b)) for a, b in zip(string, cycle(key)))
    else:
        # Python 3 bytes objects contain integer values in the range 0-255
        return bytes([a ^ b for a, b in zip(string, cycle(key))])


# ------------------- HELPER FUNCTIONS --------------------------
async def isAdmin(member):
    admin = False
    async def one_iteration(role):
        if "Thanos" == role.name:
            admin = True
    coros = [one_iteration(role) for role in member.roles]
    await asyncio.gather(*coros)

# ----------------- BOT COMMANDS ----------------------------

if(platform.uname()[1]=="raspberrypi" or platform.uname()[1]=="pi-hole"):
    bot = commands.Bot(command_prefix="!", status=discord.Status.idle, activity=discord.Game(name="Arga ubåtsljud intesifieras..."))
else:
    bot = commands.Bot(command_prefix="l:", status=discord.Status.idle, activity=discord.Game(name="Arga ubåtsljud intesifieras..."))

bot.remove_command("help")

@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Letar efter boken"))
    channel = bot.get_channel(IDs.get("ture-har-ordet"))
    if(isLocal == False):
        await channel.send(f"Jag har återvänt till staden, min senaste ritning av den nya bron finner du här: <https://github.com/AndreasH96/Discord-bot-ture/commit/{bot_version}>")

@bot.command()
async def boken1(ctx):
    await ctx.channel.send("Ge mig boken!")

@bot.command()
async def drinking_game(ctx):
    await ctx.channel.send("""Ååh! Skrotnisse Drinking-game! Som jag har längtat! :beers: \n 
Följande regler gäller... Ta en klunk när:
    Någon säger "bok/boken" :book:
    Någon säger "eremit" :older_man:
    Kalle spelar musik :musical_score:
    Ture Björkman skrattar :rofl:
    Bertil Enstöring gnäller om att han aldrig får vara ifred/säger att han vill vara ifred :angry:
    Någon/någonting flyger :flying_saucer:
    Tures mamma är i bild :older_woman:
    Ture besöker polisen :police_officer:
    Någon använder magi :mage:
    Nisse och Bertil samtalar över radio :radio:
    Nisse meckar/lagar något :wrench:
    Varje gång de har riktiga händer istället gör dockhänder :open_hands:
    Ta en shot när :milk:
    Någon talar till tittarna :eyes:
    Någon förvandlas till något annat :crystal_ball:
    Någon äter tårta :cake:
    Någonting kraschlandar :fire:
    Bertil tvingas byta bostad :house:

Skriv `!skrotnisse 1` för att få första avsnittet!
""")

@bot.command()
async def skrotnisse(ctx, *, arg):
    if(arg == "1"):
        await ctx.channel.send("[Avsnitt 1](https://www.oppetarkiv.se/video/9533973/skrotnisse-och-hans-vanner-avsnitt-1-av-13)")
    elif(arg == "2"):
        await ctx.channel.send("[Avsnitt 2](https://www.oppetarkiv.se/video/9534233/skrotnisse-och-hans-vanner-avsnitt-2-av-13)")
    elif(arg == "3"):
        await ctx.channel.send("[Avsnitt 3](https://www.oppetarkiv.se/video/9534137/skrotnisse-och-hans-vanner-avsnitt-3-av-13)")
    elif(arg == "4"):
        await ctx.channel.send("[Avsnitt 4](https://www.oppetarkiv.se/video/9534413/skrotnisse-och-hans-vanner-avsnitt-4-av-13)")
    elif(arg == "5"):
        await ctx.channel.send("[Avsnitt 5](https://www.oppetarkiv.se/video/9534053/skrotnisse-och-hans-vanner-avsnitt-5-av-13)")
    elif(arg == "6"):
        await ctx.channel.send("[Avsnitt 6](https://www.oppetarkiv.se/video/9534097/skrotnisse-och-hans-vanner-avsnitt-6-av-13)")
    elif(arg == "7"):
        await ctx.channel.send("[Avsnitt 7](https://www.oppetarkiv.se/video/9534197/skrotnisse-och-hans-vanner-avsnitt-7-av-13)")
    elif(arg == "8"):
        await ctx.channel.send("[Avsnitt 8](https://www.oppetarkiv.se/video/9534109/skrotnisse-och-hans-vanner-avsnitt-8-av-13)")
    elif(arg == "9"):
        await ctx.channel.send("[Avsnitt 9](https://www.oppetarkiv.se/video/9534245/skrotnisse-och-hans-vanner-avsnitt-9-av-13)")
    elif(arg == "10"):
        await ctx.channel.send("[Avsnitt 10](https://www.oppetarkiv.se/video/9534425/skrotnisse-och-hans-vanner-avsnitt-10-av-13)")
    elif(arg == "11"):
        await ctx.channel.send("[Avsnitt 11](https://www.oppetarkiv.se/video/9534297/skrotnisse-och-hans-vanner-avsnitt-11-av-13)")
    elif(arg == "12"):
        await ctx.channel.send("[Avsnitt 12](https://www.oppetarkiv.se/video/9534373/skrotnisse-och-hans-vanner-avsnitt-12-av-13)")
    elif(arg == "13"):
        await ctx.channel.send("[Avsnitt 13](https://www.oppetarkiv.se/video/9534257/skrotnisse-och-hans-vanner-avsnitt-13-av-13)")
    else:
        await ctx.channel.send("Hörru! Blir inga avsitt om jag inte förstår vad du menar!")


@bot.command()
async def help(ctx):
    await ctx.channel.send(""" Följande kommandon kan jag:
    ```
    !help
    !boken
    !drinking_game
    !skrotnisse 1      (1 är avsnitt 1 osv)
    ```
    """)

@bot.command()
async def info_message_food(ctx):
    member = ctx.message.author
    if isAdmin(member):
        channel = bot.get_channel(734866223744942160)
        await channel.send(messages["info_message_food"]["message"])

@bot.event
async def on_raw_reaction_add(payload):
    channels = [727220856937513031, 734866336404209665]
    if(payload.message_id == 734888243744473208):
        member = bot.get_user(payload.user_id)
        if(str(payload.emoji) == "✅"):
            for channelID in channels:
                channel = bot.get_channel(channelID)
                await channel.set_permissions(member, read_messages=True, send_messages=True, manage_messages=True, embed_links=True, attach_files=True, mention_everyone=True, add_reactions=True)
                #await member.create_dm()
                #await member.send(f"Thanks for accepting the rules of this server. You will now get a URL to authenticate yourself against.\nTo authenticate open this website: https://odethh.se/register/?ID={secret}\nThis link will only work one time. If you fail for some reason you will have to press the :white_check_mark: in #welcome again. Once you're done with this you will have access to your classes.")
        else:
            channel = bot.get_channel(payload.channel_id)
            async for elem in channel.history():
                await elem.remove_reaction(payload.emoji,member)

#--------- TO START MASTER BOT --------------
if(platform.uname()[1]=="raspberrypi" or platform.uname()[1]=="pi-hole"):
    bot_version = sys.argv[2]
    isLocal = False
    try:
        key = base64.encodebytes(bytes(sys.argv[1], encoding="UTF-8"))
        decryptedHost = base64.decodebytes(xor_strings(bytes(encryptedKeys.get("live"), encoding="UTF-8"), key)).decode("UTF-8")
        bot.run(decryptedHost)
        decryptedHost = 0
    except Exception as e:
        print(f"Fail master bot: {e}")

#--------- TO START BOT LOCAL BOT 01 ----------------
elif(sys.argv[1] == "01"):
    isLocal = True
    try:
        key = base64.encodebytes(bytes(sys.argv[2], encoding="UTF-8"))
        decryptedHost = base64.decodebytes(xor_strings(bytes(encryptedKeys.get("local"), encoding="UTF-8"), key)).decode("UTF-8")
        bot.run(decryptedHost)
        decryptedHost = 0
    except Exception as e:
        print(f"Fail local bot: {e}")

