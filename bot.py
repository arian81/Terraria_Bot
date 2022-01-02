import discord
import subprocess
import os
from discord.ext import commands 
import json
def checkStatus():
    process = subprocess.getstatusoutput(f'ps aux | grep mono')
    for i in process:
        try:
            if "mono TerrariaServer.exe" in i:
                return True
            else:
                return False
        except TypeError:
            pass
client = discord.Client()
bot = commands.Bot(command_prefix="/")


@bot.command(
    help = "Tells you whether the server is working or not",
    brief = "server going brrrr or not"
)
async def status(message):
    if checkStatus:
        await message.channel.send("Server is operational :)")
    else:
        await message.channel.send("Server is down :( Arian already got a notification, he's on it")

@bot.command(
    help = "Asking for features to be added to the server or bot",
    brief = "Comments and requests go here"
)
async def request(message, req = "blob"):
    with open("todo.txt","a") as file:
        if req == "blob":
            reply = await message.channel.fetch_message(message.message.reference.message_id)
            file.write(reply.content + "\n")
        else:
            file.write(req + "\n")
    await message.channel.send("Your feature requst has been added. Arian is gonna take a look at it and implement it if he's not being lazy.")


@bot.command(
    help = "Adds / Updates someone's steam id",
    brief = "steam ids, gotta catch em all"
)
async def add_sid(message, name, sid):
    with open("db.json","r+") as file:
        jsonData = json.load(file)
        if name in jsonData["steam_ids"].keys():
            jsonData["steam_ids"][name] = sid
        else:
            jsonData["steam_ids"].update({name:sid})
        file.seek(0)
        json.dump(jsonData,file)
    await message.channel.send("Welcome to the steam club boi")

@bot.command(
    help = "Get a list of all steam ids or the steam id of someone specific",
    brief = "Snoop into collected steam id databse and see what's up"
)
async def list_sid(message, name = "all"):
    with open("db.json","r") as file:
        jsonData = json.load(file)
        if name == "all":
            returnStr = ""
            for key in jsonData["steam_ids"].keys():
                returnStr += (key + " : " + jsonData["steam_ids"][key] + "\n")
            await message.channel.send(returnStr)
        else:
            await message.channel.send(jsonData["steam_ids"][name])

@bot.command(
    help = "Deletes an entry from database",
    brief = "Helps you in case of stoopid smol brain mistakes"
)
async def del_sid(message, name):
    with open("db.json","r") as file:
        jsonData = json.load(file)
        if name in jsonData["steam_ids"].keys():
            del jsonData["steam_ids"][name]
        else:
            await message.channel.send("That name is not in the database.")
    with open("db.json","w") as file:
        json.dump(jsonData,file)
        await message.channel.send("Hopefully you're just fixing your name or sth and not actually leaving the steam club.")

@bot.command(
    help = "Bruh!",
    brief = "Bruh!"
)
async def bruh(message):
    await message.channel.send("Bruh!")
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}. Locked and loaded")

@bot.event
async def on_message(message):
    
    if message.author == client.user:
        return
    if "69" in message.content:
        await message.channel.send("Nice!")
    if "420" in message.content:
        await message.channel.send(file = discord.File("./assets/snoop.gif"))
    await bot.process_commands(message)

with open("token.txt","r") as file:
    token = file.read()    
bot.run(token)