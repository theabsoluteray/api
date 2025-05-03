import discord
from discord.ext import commands
import shutil
import requests
import os
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    await bot.change_presence(activity=discord.Game(name="rayuwu"))



@bot.command()
async def fetch(ctx, key: str, filename: str):
    await ctx.send(f"Fetching `{filename}` using key `{key}`...")

   
    res = requests.get("http://127.0.0.1:5000/get-image", params={"key": key, "filename": filename})

    if res.status_code == 200:
        filepath = f"./content/{filename}"

        if os.path.exists(filepath):
            await ctx.send(f"File ready! Uploading `{filename}`...", file=discord.File(filepath))
            os.remove(filepath) 
        else:
            await ctx.send("File was not found in content directory after fetch.")
    else:
        await ctx.send(f"Failed to fetch file. Server responded with: {res.status_code} - {res.text}")
tkn = os.getenv("token")
bot.run(tkn)