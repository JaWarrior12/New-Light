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
#from dpyConsole import Console

#Lists
import lists
#Auth For Leadership Commands
#authorized = lists.authorized
banned = lists.banned
developers = lists.developers
DEV_SERVER_ID = lists.DEV_SERVER_ID 

#PLEXUS_SERVER_ID = 1070759679543750697 #Actual Plexus Server ID
#PLEXUS_CHANNEL_ID = 1264242324482031707 #Actual Plexus Reports Channel ID
PLEXUS_SERVER_ID = 1031900634741473280 #NLD Server ID
PLEXUS_CHANNEL_ID = 1045129470287294504 #NLD Server dev-bot-commands channel ID


#tz = pytz.timezone('America/New_York')
utc=timezone.utc
tmes=tme(hour=0,minute=20,tzinfo=utc)

def readPS():
    return loads(open('.../NLDB/plexusSystems.json', 'r').read())

def setPS(data):
    with open(".../NLDB/plexusSystems.json", "w") as f:
        f.write(dumps(data))

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
  
  @commands.command(name="testRDTR",help="Tests the runDailyTransferReport script.")
  async def testRDTR(self,ctx,year=None,month=None,day=None):
    if ctx.message.author.id in developers:
      await self.runDailyTransferReport(self,year,month,day)
    else:
      await ctx.send("This is a DEVELOPER ONLY command.")
  
  @tasks.loop(time=tmes)
  async def runDailyTransferReport_TimerLoop(self):
    await self.runDailyTransferReport(self,None,None,None)
  
  @staticmethod
  async def runDailyTransferReport(self,year=None,month=None,day=None):
    print("Starting Plexus Daily Transfer Report Script")
    data = lists.readFile("plexusSystems")
    print(data)
    shipsToLoop=data["clanShips"]
    log_file_name=None
    logFile=None
    if year is None:
      year=datetime.today().year
      month=datetime.today().month
      day=datetime.today().day
    PlexusServer = self.bot.get_guild(PLEXUS_SERVER_ID)
    print(PlexusServer)
    PlexusReportChannel = await PlexusServer.fetch_channel(PLEXUS_CHANNEL_ID)
    print(PlexusReportChannel)
    try:
      jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{int(year)}_{int(month)}_{int(day)}/log.json.gz')
      shipData = lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{int(year)}_{int(month)}_{int(day)}/ships.json.gz')
      log_file_name=f"Plexus_Daily_Transfers.txt"
      for ship in shipsToLoop:
        hexcode="{"+ship+"}"
        def find_route(data, route_no):
          return list(filter(lambda x: x.get("src") == route_no, data))
        route = find_route(jsondata,hexcode)
        url = "https://pub.drednot.io/test/econ/item_schema.json"
        itemSchema = loads(requests.get(url).content)
        def findItemName(itemId):
          return list(filter(lambda x: x.get('id') == itemId, itemSchema))
        def shipNameLookup(hex):
          return list(filter(lambda x: x.get('hex_code') == hex, shipData))
        items={}
        for log in route:
          itemName=findItemName(log["item"])[0]["name"]
          if itemName not in list(items.keys()):
            items.update({itemName:0})
        for logB in route:
          itemName=findItemName(logB["item"])[0]["name"]
          items[itemName]+=logB["count"]
        #print(route)
        #print(items)
        with open(log_file_name, "a", encoding="utf-8") as logFile:
          for x in route:
            timeConversion=datetime.fromtimestamp(x["time"]).strftime('%c')
            if x["serv"]==0:
              serverConversion="US"
            elif x["serv"]==1:
              serverConversion="EU"
            elif x["serv"]==2:
              serverConversion="AS"
            else:
              serverConversion="??"
            itemNameConversion=findItemName(int(x["item"]))
            srcShipConversion=shipNameLookup(x["src"].replace("{","").replace("}",""))[0]
            srcShipHex="{"+srcShipConversion["hex_code"]+"}"
            srcShipConversion={"name":srcShipConversion["name"],"hex_code":srcShipHex}
            #print(srcShipConversion)
            if x["dst"]=="killed":
              dstShipConversion={"name":"Destroyed","hex_code":""}
            else:
              dstShipConversion=shipNameLookup(x["dst"].replace("{","").replace("}",""))[0]
              dstShipHex="{"+dstShipConversion["hex_code"]+"}"
              dstShipConversion={"name":dstShipConversion["name"],"hex_code":dstShipHex}
            logFile.write(f"{serverConversion} {timeConversion} UTC {x["zone"]} {srcShipConversion["name"]} {srcShipConversion["hex_code"]} sent {x["count"]} {findItemName(x["item"])[0]["name"]} to {dstShipConversion["name"]} {dstShipConversion["hex_code"]} \n")
    except Exception as e:
      print(e)
      e_type, e_object, e_traceback = sys.exc_info()

      e_filename = os.path.split(
          e_traceback.tb_frame.f_code.co_filename
      )[1]

      e_message = str(e)

      e_line_number = e_traceback.tb_lineno

      print(f'exception type: {e_type}')

      print(f'exception filename: {e_filename}')

      print(f'exception line number: {e_line_number}')

      print(f'exception message: {e_message}')
    if log_file_name != None:
      message=f"Plexus Daily Transfer Report For {datetime.now()}"
      await PlexusReportChannel.send(message,file=discord.File(log_file_name))
      os.remove(log_file_name)
    print("Plexus Daily Transfer Report Script Finished")
  
async def setup(bot: commands.Bot):
    await bot.add_cog(PlexusCmds(bot))