#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
import io
import os
import aiohttp
from io import BytesIO
import discord
import platform
import base64
import datetime
from discord.ext import commands
import sys
import asyncio
from itertools import cycle
import json
import wolframalpha
import random
import requests
import pathlib
from gpiozero import CPUTemperature, LoadAverage, DiskUsage
import http.client, urllib.request, urllib.parse, urllib.error, base64
import os
from random import randint

if platform.uname()[4] == "aarch64":
    import os
    os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')
    from gpiozero import CPUTemperature, LoadAverage, DiskUsage

encryptedKeys = {"live": "\r\x03I<?\x12\x01\t\x1e2)sk2\\\r&7'n5&S\x18\\91#X\x1e\x1f x\x14%Y/\x0eDo<jG+\x05a6\x07\x08\x08Yz\x08\x00w1\x08\x02\x0c\x0c\x03\x01u\x0c^#4@=\r/n!\x1a<\x157[7\x0e\x04x",
                "local": "\r\x03I<?\x02\x05N\x1e>\x07ro5\x01\n&6\x05n6\x18[{d95=k4\x0f x\x14%Y(n;7<jG\x0c5p.\x17?&{C;\x17{D\x00ezN\x1e<\x1fvP5/}$k\r}\x1a\x05\x1a\x1c7^\x11 \x04x"}

askTureMessages =["Hmm... den var klurig. Jag ska kolla upp detta i boken!","Kunskap är makt! Nu tar vi över världen. Vänta lite bara...",
                "Jaha är du här och stör igen... Ja jag får väl kolla up det då.","Jag är stadsingenjör, jag kan en del saker. Vänta ska du få se!"]
askTureInfoNotFoundMessages =["Ajaj Hasse detta hittade jag inget om i boken! Bättre lycka nästa gång.","Den där nedrans eremiten har tagit tillbaka boken, du får klara dig själv.",
                "Rackarns bananer nu är det jag som får skämmas. Här står ingenting om din fråga.", "Vad förväntar du dig av mig!? Jag är bara en sketen bot skriven av några imbeciller."]

IDs = {"serverID":467039975276281856, "ture-har-ordet":729990369525235772, "vmguld-i-skitsnack":467039975276281858, "bot-testing":768443897352683530}

IDs = {"serverID":467039975276281856, \
        "ture-har-ordet":729990369525235772, \
        "vmguld-i-skitsnack":467039975276281858, \
        "bot-testing":768443897352683530, \
        "matkanalen":727220856937513031, \
        "grogghörnan":734866336404209665, \
        "information_mat": 734866223744942160, \
        "köpstopp":769180472189911071, \
        "role_Thanos":727146183822278697, \
        "role_Köpstopp":727147167680036894, \
        "role_GH":735083349097316352, \
        "role_Familjen":763487940667244565, \
        "role_ByggareBob":763487940667244565}


isLocal = True
botVersion = 0.00

with open("/var/lib/jenkins/wolfram.key",encoding='utf-8',mode="r") as key:
    wolframKey = key.read()
    wolframKey = wolframKey.replace("\n", "")


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

intents = discord.Intents.default()  # All but the two privileged ones
intents.members = True

if(platform.uname()[1]=="raspberrypi" or platform.uname()[1]=="pi4-arch"):
    bot = commands.Bot(command_prefix="!", status=discord.Status.idle, activity=discord.Game(name="Arga ubåtsljud intesifieras..."), intents=intents)
else:
    bot = commands.Bot(command_prefix="l:", status=discord.Status.idle, activity=discord.Game(name="Arga ubåtsljud intesifieras..."), intents=intents)

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
async def askTure(ctx , *, arg):

    # init client
    client = wolframalpha.Client(wolframKey)
    
    # send first message to user
    await ctx.channel.send(askTureMessages[random.randint(0,len(askTureMessages)-1)])
    
    # query wolfram alpha
    result = client.query(arg) 
    # get the main pod of data
    resultPods = result.get("pod")
    message = []
    titleAmount = 0
    images = []
    try: 
        # for each pod add pod title and images from its sub pods
        for pod in resultPods:
            message.append(pod.get("@title"))
            titleAmount +=1
            subpod = pod.get("subpod")
            if(type(subpod) == list):
                for childpod in subpod:
                    response = requests.get(childpod.get("img").get("@src"))
                    img= Image.open(BytesIO(response.content))
                    images.append(img)
                    message.append(img)
            elif (type(subpod) == dict):
                response = requests.get(subpod.get("img").get("@src"))
                img= Image.open(BytesIO(response.content))
                images.append(img)
                message.append(img)

        # adjust final image height and width
        widths,heights = zip(*(i.size for i in images))
        totalHeight = sum(heights) + titleAmount * 18
        maxWidth = max(widths)
        newImage = Image.new('RGB',(maxWidth,totalHeight),color="white")
        yOffset = 0 
        imageDraw = ImageDraw.Draw(newImage)
        # Create font and add titles to final images
        font = ImageFont.truetype("Verdana.ttf",14)
        for field in message:
            if type(field) == str:
                imageDraw.text((5,yOffset),field,font=font,fill="black")
                yOffset +=18
            else :
                newImage.paste(field,(0,yOffset))
                yOffset += field.size[1]
        
        # create temp file name 
        tempFileName = "{}.png".format(random.randint(1,10000))
        # save temp file
        newImage.save(tempFileName,'PNG')
        imagePath = "{}/{}".format(str(pathlib.Path().absolute()),tempFileName)
        # create embed and set file & image
        embed = discord.Embed(title="Här har du, lämna mig ifred nu", color=0x00ff00) #creates embed
        f = discord.File(imagePath, filename=tempFileName)
        embed.set_image(url="attachment://{}".format(tempFileName))
        
        # send image and remove temp file
        await ctx.send(file=f, embed=embed)
        os.remove(imagePath)

    except:
         await ctx.channel.send(askTureInfoNotFoundMessages[random.randint(0,len(askTureInfoNotFoundMessages)-1)])



@bot.command()
async def boken(ctx):
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

    ---------------------------------------

    Admin kommandon
    !pi [temp, load, disk, all]
    !info_message_food
    !info_message_kopstopp
    ```
    """)

@bot.command()
async def info_message_food(ctx):
    member = ctx.message.author
    if isAdmin(member):
        channel = bot.get_channel(IDs.get("information_mat"))
        await channel.send(messages["info_message_food"]["message"])

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    rolesDict = {role.name : role for role in guild.roles}
    member = guild.get_member(payload.user_id)
    user = bot.get_user(payload.user_id)
    if(payload.message_id == 769172891702263828):
        if(str(payload.emoji) == "✅"):
            for channelID in [IDs.get("matkanalen"), IDs.get("grogghörnan")]:
                channel = bot.get_channel(channelID)
                await channel.set_permissions(user, read_messages=True, send_messages=True, manage_messages=True, embed_links=True, attach_files=True, mention_everyone=True, add_reactions=True) 
        else:
            channel = bot.get_channel(payload.channel_id)
            async for elem in channel.history():
                await elem.remove_reaction(payload.emoji,member)
    elif(payload.message_id == 769218692948295721):
        for roleName in ["Köpstopp", "GH", "Familjen"]:
            await member.remove_roles(rolesDict.get(roleName))
            
        if(str(payload.emoji) == "\U0001F986"):
            role = rolesDict.get("Köpstopp")
            await member.add_roles(role)
        elif(str(payload.emoji) == "🐦"):
            role = rolesDict.get("GH")
            await member.add_roles(role)
        elif(str(payload.emoji) == "👪"):
            role = rolesDict.get("Familjen")
            await member.add_roles(role)

@bot.command()
async def info_message_kopstopp(ctx):
    member = ctx.message.author
    if isAdmin(member):
        channel = bot.get_channel(IDs.get("köpstopp"))
        await channel.send(messages["info_message_köpstopp"]["message"])


@bot.command()
async def pi(ctx, *, args):
    member = ctx.message.author
    channel = bot.get_channel(IDs.get("bot-testing"))
    if(isAdmin(member)):
        await ctx.channel.send("Informationen skickas i #bot-testing")
        if args == "temp":
            cpu = CPUTemperature()
            cpu_temp = round(cpu.temperature)
            await channel.send(f"Temp: {cpu_temp}°C")
        elif args == "load":
            load = LoadAverage()
            load_avg = round(load.load_average*100)
            await channel.send(f"Load: {load_avg}%")
        elif args == "disk":
            disk = DiskUsage()
            disk_usage = round(disk.usage)
            await channel.send(f"Disk: {disk_usage}%")
        elif args == "all":
            cpu = CPUTemperature()
            cpu_temp = round(cpu.temperature)
            load = LoadAverage()
            load_avg = round(load.load_average*100)
            disk = DiskUsage()
            disk_usage = round(disk.usage)
            await channel.send(f"Temp: {cpu_temp}°C \nLoad: {load_avg}% \nDisk: {disk_usage}%")
        else:
            await channel.send(f"Jag förstår inte argumentet: {args} \n Jag kan följande: [temp, load, disk, all]")
    else:
        await ctx.channel.send("Endast individer av exceptionell rank har tillgång till denna funktion!")

@bot.command()
async def snapsvisa(ctx):
    with open('snapsvisor.json', encoding='utf-8') as f:
        data = json.load(f)
        songs = data["snapsvisor"]["visor"]
        random_song = randint(0, len(songs)-1)
    await ctx.channel.send(songs[random_song]["visa"])

#--------- TO START MASTER BOT --------------
if(platform.uname()[1]=="raspberrypi" or platform.uname()[1]=="pi4-arch"):
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
