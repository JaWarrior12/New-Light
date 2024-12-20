import os, discord, sys
from aiohttp import DataQueue
import time as timea
import traceback
import asyncio
import pytz
import datetime
from datetime import datetime, timedelta, timezone
from datetime import time as tme
#from apscheduler.schedulers.background import BackgroundScheduler
from threading import Timer
import urllib.request
import requests
import gzip
#from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.utils import get
from discord import Member
from json import loads, dumps
from startup import startup

# Translator Library
#from googletrans import Translator
from deep_translator import GoogleTranslator

#Lists
import lists
#Auth For Leadership Commands
#authorized = lists.authorized
banned = lists.banned
developers = lists.developers
DEV_SERVER_ID = lists.DEV_SERVER_ID 

#tz = pytz.timezone('America/New_York')
utc=timezone.utc
tmes=tme(hour=0,minute=10,tzinfo=utc)

class TranslationSystem(commands.Cog, name="Translation System Commands",description="Commands For The Translation System"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if self.bot.application_id == 974045822167679087:
            pass
    def cog_unload(self):
        if self.bot.application_id == 974045822167679087:
            pass
    
    @commands.command(name="translate", aliases=["tr"])
    async def translate(self, ctx, text):
        translator = GoogleTranslator(source='auto', target='russian')
        response=translator.translate(text=text)
        await ctx.send(response)

    @commands.command(name="configTranslate",aliases=["cr","configT"],help="Settings manager for all translation settings. `targetLang` MUST be the 2 letter language code!! Valid keys: list, add (Add channel), remove (Remove Channel), modify (Modify CHANNEL)")
    async def configTranslate(self,ctx,option,channel=None,targetLang=None,onBool=None):
        if str(ctx.message.author.id) not in banned:
            chk = lists.checkperms(ctx)
            if chk == True:
                data=lists.readFile("translationConfig")
                if option=="list":
                    e = discord.Embed(title="Translation Configuration Settings For "+ctx.message.guild.name)
                    e.add_field(name="Translation Active?",value=lists.readdataE()[str(ctx.message.guild.id)]["translationBool"],inline=False)
                    for item in data[str(ctx.message.guild.id)]["langChannels"]:
                        e.add_field(name="Channel Name",value=ctx.guild.get_channel(item[0]).name,inline=True)
                        e.add_field(name="Channel Mention",value=ctx.guild.get_channel(item[0]).mention,inline=True)
                        e.add_field(name="Channel ID",value=item[0],inline=True)
                        e.add_field(name="Target Language",value=item[1],inline=True)
                        e.add_field(name="Channel Actively Translated To?",value=item[3],inline=True)
                    await ctx.send(embed=e)
                elif option=="add":
                    chanID=None
                    chaneName=None
                    chanMen=None
                    if type(channel)==discord.GuildChannel:
                        chanID=channel.id
                        chanName=channel.name
                        chanMen=channel.mention
                    elif type(channel)==int:
                        chanID=channel
                        chanName=server.get_channel(chanID).name
                        chanMen=server.get_channel(chanID).mention
                    else:
                        return await ctx.send(f"Sorry, {channel} is not a valid input. Please mention your target channel or use the channel's ID.")
                    if len(targetLang)==2:
                        pass
                    else:
                        return await ctx.send(f"Sorry, {targetLang} is not a valid input. Please provide the 2 letter language code for your target language.")
                    data[str(server.id)]["langChannels"].append([chanID,targetLang,True])
                    lists.setFile("translationConfig",data)
                    await ctx.send(f"{chanMen} has been added to Auto-Translate for the target language {targetLang}")

            else:
                await ctx.send("Sorry, only authorized leaders can use this command.")
        else:
            await ctx.send("Sorry, You are banned from using New Light. Contact JaWarrior if you believe this to be a mistake.")

    @commands.Cog.listener()
    async def on_message(self,message):
        server=message.guild
        data=lists.readFile("translationConfig")
        if message.guild!=None and lists.readdataE()[str(server.id)]["translationBool"]:
            translator = GoogleTranslator(source='auto', target='russian')
            langChannels=data[str(server.id)]["langChannels"]
            for channel in langChannels:
                chanID=channel[0]
                targetLang=channel[1]
                targetChanBool=channel[2]
                if targetChanBool:
                    targetChan=server.get_channel(chanID)
                    translator.target=str(targetLang)
                    response=translator.translate(text=message.content)
                    await targetChan.send(response,embeds=message.embeds,files=message.attachments)
                else:
                    continue
    

async def setup(bot: commands.Bot):
    await bot.add_cog(TranslationSystem(bot))