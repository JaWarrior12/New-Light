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

    @commands.Cog.listener()
    async def on_message(self,message):
        server=message.guild
        data=lists.readFile("translationConfig")
        if message.guild!=None and data[str(server.id)]["translationBool"]:
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