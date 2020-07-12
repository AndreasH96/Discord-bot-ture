import discord
import platform
import base64
import datetime
from discord.ext import commands
import sys
import asyncio
from itertools import cycle

encryptionKeys = {"live": "\r\x03I<?\x12\x01\t\x1e2)sk2\\\r&7'n5&S\x18\\91#X\x1e\x1f x\x14%Y/\x0eDo<jG+\x05a6\x07\x08\x08Yz\x08\x00w1\x08\x02\x0c\x0c\x03\x01u\x0c^#4@=\r/n!\x1a<\x157[7\x0e\x04x", "local": ""}

IDs = {"serverID":467039975276281856, "ture-har-ordet":729990369525235772, "vmguld-i-skitsnack":467039975276281858}

isLocal = True
botVersion = 0.00

# ------------------------------- Encryption -------------------------------

def xor_strings(string, theKey):
    """xor two strings together"""
    if isinstance(string, str):
        # Text strings contain single characters
        return b"".join(chr(ord(a) ^ ord(b)) for a, b in zip(string, cycle(key)))
    else:
        # Python 3 bytes objects contain integer values in the range 0-255
        return bytes([a ^ b for a, b in zip(string, cycle(key))])

# --------------------------------------------------------------------------

# ------------------- HELPER FUNCTIONS --------------------------
async def isAdmin(member):
    admin = False
    for role in member.roles:
        if "admin" == role.name:
            admin = True
    return admin

# ----------------- BOT COMMANDS ----------------------------

if(platform.uname()[1]=="raspberrypi"):
    bot = commands.Bot(command_prefix="!", status=discord.Status.idle, activity=discord.Game(name="Arga ubåtsljud intesifieras..."))
else:
    bot = commands.Bot(command_prefix="l:", status=discord.Status.idle, activity=discord.Game(name="Arga ubåtsljud intesifieras..."))


@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Letar efter boken"))
    channel = bot.get_channel(IDs.get("ture-har-ordet"))
    if(isLocal):
        await channel.send(f"Jag har återvänt till staden!")
    else:    
        await channel.send(f"Jag har återvänt till staden, min senaste ritning av den nya bron finner du här: https://github.com/AndreasH96/Discord-bot-ture/commit/{bot_version}")


#--------- TO START MASTER BOT --------------
if(platform.uname()[1]=="raspberrypi"):
    bot_version = sys.argv[2]
    isLocal = False
    try:
        key = base64.encodebytes(bytes(sys.argv[1], encoding="UTF-8"))
        decryptedHost = base64.decodebytes(xor_strings(bytes(encryptionKeys.get("live"), encoding="UTF-8"), key)).decode("UTF-8")
        bot.run(decryptedHost)
        decryptedHost = 0
    except Exception as e:
        print(f"Fail master bot: {e}")

#--------- TO START BOT LOCAL BOT 01 ----------------
elif(sys.argv[1] == "01"):
    isLocal = True
    # SPECAIL CASE IF LOCAL BOT ISN'T RUNNING ON UNIX SYSTEM
    if(platform.uname()[0] != "Linux"):
        try:
            #Thread(target=bot.run,args=(local,)).start()
            key = base64.encodebytes(bytes(sys.argv[2], encoding="UTF-8"))
            decryptedHost = base64.decodebytes(xor_strings(bytes(encryptionKeys.get("live"), encoding="UTF-8"), key)).decode("UTF-8")
            bot.run(decryptedHost)
            decryptedHost = 0
        except Exception as e:
            print("Error: unable to start event loop (local 01)")
            print(e)
    # TO START LOCAL BOT ON UNIX SYSTEM
    else:
        try:
            key = base64.encodebytes(bytes(sys.argv[2], encoding="UTF-8"))
            decryptedHost = base64.decodebytes(xor_strings(bytes(encryptionKeys.get("live"), encoding="UTF-8"), key)).decode("UTF-8")
            bot.run(decryptedHost)
            decryptedHost = 0
        except Exception as e:
            print(f"Fail local bot: {e}")

