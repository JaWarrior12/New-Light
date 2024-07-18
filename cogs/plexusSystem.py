import os, discord
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
#from dpyConsole import Console

#Lists
import lists
#Auth For Leadership Commands
#authorized = lists.authorized
banned = lists.banned
developers = lists.developers
DEV_SERVER_ID = lists.DEV_SERVER_ID 

PLEXUS_SERVER_ID = 1070759679543750697


#tz = pytz.timezone('America/New_York')
utc=timezone.utc
tmes=tme(hour=0,minute=20,tzinfo=utc)

class PlexusCmds(commands.Cog, name="Plexus Commands",description="Commands For Plexus"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.runDailyTransferReport_TimerLoop.start()
    #if bot.application_id != 975858537223847936:
      #self.verifyschedule.start()
        #pass
  def cog_unload(self):
    self.runDailyTransferReport_TimerLoop.cancel()
    #if self.bot.application_id != 975858537223847936:
      #pass
      #self.verifyschedule.cancel()
    #else:
    #pass
  
  def is_plexus_server():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.id == PLEXUS_SERVER_ID or ctx.author.id in lists.developers
    return commands.check(predicate)
  
  @tasks.loop(time=tmes)
  async def runDailyTransferReport_TimerLoop(self):
    await self.runDailyTransferReport(self)
  
  @staticmethod
  async def runDailyTransferReport(self):
     pass
  
async def setup(bot: commands.Bot):
    await bot.add_cog(PlexusCmds(bot))