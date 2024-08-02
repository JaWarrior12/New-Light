from multiprocessing.spawn import old_main_modules
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
ALLOWED_SERVERS = [1070759679543750697,1031900634741473280]

NON_SHIP_ENTRIES=["Aqua Shielder","Red Sentry","Blue Rusher","The Shield Master","Shield Helper","Red Sniper",'Yellow Hunter',"The Lazer Enthusiast","The Coward","Orange Fool","Yellow Mine Guard","block - iron mine","bot - zombie tank","giant rubber ball","bot - zombie","block - vault","block - flux node","bot - zombie hunter","bot - zombie boss","block - treasure diamond"]


#tz = pytz.timezone('America/New_York')
utc=timezone.utc
tmes=tme(hour=0,minute=10,tzinfo=utc)

def readPS():
    return loads(open('.../NLDB/plexusSystems.json', 'r').read())

def setPS(data):
    with open(".../NLDB/plexusSystems.json", "w") as f:
        f.write(dumps(data))

class PlexusCmds(commands.Cog, name="Plexus Commands",description="Commands For Plexus"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    #self.runDailyTransferReport_TimerLoop.start
    #print(self.bot.application_id)
    if self.bot.application_id == 974045822167679087:
      self.runDailyTransferReport_TimerLoop.start()
      print("start trackLog loop")
      #pass
  def cog_unload(self):
    if self.bot.application_id == 974045822167679087:
      #pass
      self.runDailyTransferReport_TimerLoop.cancel()
    #else:
    #pass
  
  def is_plexus_server():
    def predicate(ctx):
        return ctx.guild is not None or ctx.author.id in lists.developers #and ctx.guild.id in ALLOWED_SERVERS
    return commands.check(predicate)
  
  @commands.command(name="testRDTR",help="Tests the runDailyTransferReport script.")
  async def testRDTR(self,ctx,year=None,month=None,day=None):
    if ctx.message.author.id in developers:
      await self.runDailyTransferReport(self,year,month,day)
    else:
      await ctx.send("This is a DEVELOPER ONLY command.")

  @commands.command(name="updateTrackList",aliases=["utl"],help="Add or Remove a ship from the track list; also can display the current trck list. Functions :add/remove/list")
  @commands.check_any(is_plexus_server())
  async def updateTrackList(self,ctx,function,hex=None):
    chk = lists.checkperms(ctx)
    if chk:
      data = lists.readFile("plexusSystems")
      if function.lower() == "add":
        hex=hex.upper()
        if hex not in data[str(ctx.guild.id)]['trackList'] and hex != None:
          data[str(ctx.guild.id)]['trackList'].append(hex)
          await ctx.send(f"Added {hex} to the track list.")
          lists.setFile("plexusSystems",data)
        else:
          await ctx.send(f"Hex {hex} is already in the track list.")
      elif function.lower() == "remove":
        hex=hex.upper()
        if hex in data[str(ctx.guild.id)]['trackList']:
          data[str(ctx.guild.id)]['trackList'].remove(hex)
          await ctx.send(f"Removed {hex} from the track list.")
          lists.setFile("plexusSystems",data)
        else:
          await ctx.send(f"Hex {hex} was not found in the track list.")
      elif function.lower() == "list":
        await ctx.send(f"{ctx.guild.name} Track List")
        trackListMsg=""
        for ship in data[str(ctx.guild.id)]['trackList']:
          trackListMsg = trackListMsg+"\n- "+ship
        await ctx.send(trackListMsg)
      else:
        await ctx.send(f"Sorry, {function} is not a valid function for this command. Valid Functions: Add/List/Remove")
  
  @tasks.loop(time=tmes)
  async def runDailyTransferReport_TimerLoop(self):
    print("Running Daily trackLog Loop!")
    await self.runDailyTransferReport(self,None,None,None)
  
  @staticmethod
  async def runDailyTransferReport(self,year=None,month=None,day=None):
    print("Starting Plexus Daily Transfer Report Script")
    data = lists.readFile("plexusSystems")
    configs=lists.readdataE()
    #print(data)
    for key in list(data.keys()):
      logChannel=configs[str(key)]["trackLogChannel"]
      shipsToLoop=data[str(key)]["trackList"]
      log_file_name=None
      logFile=None
      if year is None:
        year=datetime.today().year
        month=datetime.today().month
        day=datetime.today().day
      PlexusServer = self.bot.get_guild(int(key))
      print(PlexusServer)
      PlexusReportChannel = await PlexusServer.fetch_channel(int(logChannel))
      print(PlexusReportChannel)
      try:
        jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{int(year)}_{int(month)}_{int(day)}/log.json.gz')
        shipData = lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{int(year)}_{int(month)}_{int(day)}/ships.json.gz')
        altShipData = lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{int(year)}_{int(month)}_{int(day)}/ships.json.gz')
        log_file_name=f"Plexus_Daily_Transfers.txt"
        shipTotals={}
        receiveTotals={}
        for ship in shipsToLoop:
          oldHexcode=ship
          shipTotals.update({oldHexcode:{}})
          receiveTotals.update({oldHexcode:{}})
          hexcode="{"+ship+"}"
          def find_route(data, route_no):
            return list(filter(lambda x: x.get("src") == route_no, data))
          route = find_route(jsondata,hexcode)
          def find_dest(data, route_no):
            return list(filter(lambda x: x.get("dst") == route_no, data))
          destList = find_dest(jsondata,hexcode)
          url = "https://pub.drednot.io/prod/econ/item_schema.json"
          itemSchema = loads(requests.get(url).content)
          def findItemName(itemId):
            return list(filter(lambda x: x.get('id') == itemId, itemSchema))
          def shipNameLookup(hex):
            return list(filter(lambda x: x.get('hex_code') == hex, shipData))
          def altShipNameLookup(hex):
            return list(filter(lambda x: x.get('hex_code') == hex, altShipData))
          items={}
          destItems={}
          #Logs A,B,C Are For Receiving
          for logA in route:
            destShip=logA["dst"].replace("{","").replace("}","")
            #print(destShip)
            if destShip not in list(items.keys()):
              items.update({destShip:{}})
          #print(items)
          for logB in route:
            destShip=logB["dst"].replace("{","").replace("}","")
            itemName=str(findItemName(logB["item"])[0]["name"])
            #print(list(items[destShip].keys()))
            items.update({destShip:{str(itemName):0}})
          #print(items)
          for logC in route:
            destShip=logC["dst"].replace("{","").replace("}","")
            itemName=findItemName(logC["item"])[0]["name"]
            #print(destShip)
            #print(itemName)
            #print(logC)
            if itemName not in list(items[destShip].keys()):
              items.update({destShip:{str(itemName):0}})
            items[destShip][str(itemName)]+=logC["count"]

          #Logs D,E,F Are For Receiving Logs
          for logD in destList:
            destShip=logD["src"].replace("{","").replace("}","")
            #print(destShip)
            if destShip not in list(destItems.keys()):
              destItems.update({destShip:{}})
          #print(items)
          for logE in destList:
            destShip=logE["src"].replace("{","").replace("}","")
            itemName=str(findItemName(logE["item"])[0]["name"])
            #print(list(items[destShip].keys()))
            destItems.update({destShip:{str(itemName):0}})
          #print(items)
          for logF in destList:
            destShip=logF["src"].replace("{","").replace("}","")
            itemName=findItemName(logF["item"])[0]["name"]
            #print(destShip)
            #print(itemName)
            #print(logC)
            if itemName not in list(destItems[destShip].keys()):
              destItems.update({destShip:{str(itemName):0}})
            destItems[destShip][str(itemName)]+=logF["count"]
          shipTotals.update({oldHexcode:items})
          receiveTotals.update({oldHexcode:destItems})
          #print(receiveTotals)
        def writeToFile(sourceDict,sectionTitle,stateVar):
          #StateVar is 0 or 1, 0==Send/shipTotals, 1==Receive/receiveTotals
          with open(log_file_name, "a+", encoding="utf-8") as logFile:
            if sum(1 for _ in logFile)==0:
              logFile.write(f"--\\/--{sectionTitle}--\\/--\n")
            else:
              logFile.write(f"\n\n--\/--{sectionTitle}--\/--\n")
            shipTotalsKeys=list(sourceDict.keys())
            for hex in shipTotalsKeys:
              shipLogs=sourceDict[hex]
              #print(len(list(shipTotals[hex].keys())))
              #print(list(shipTotals[hex].keys()))
              if len(list(sourceDict[hex].keys()))==0 and stateVar==0:
                hexCode=hex
                ShipConversion=shipNameLookup(hexCode)
                altShipConversion=altShipNameLookup(hexCode)
                #print(ShipConversion)
                if len(ShipConversion)>0:
                  logFile.write(f"{ShipConversion[0]["name"]} ({ShipConversion[0]["hex_code"]}) transfered no items \n")
                else:
                  if len(altShipConversion)>0:
                    logFile.write(f"{altShipConversion[0]["name"]} ({altShipConversion[0]["hex_code"]}) transfered no items \n")
                  else:
                    logFile.write(f"{hex} transfered no items \n")
              elif len(list(sourceDict[hex].keys()))==0 and stateVar==1:
                hexCode=hex
                ShipConversion=shipNameLookup(hexCode)
                altShipConversion=altShipNameLookup(hexCode)
                #print(ShipConversion)
                if len(ShipConversion)>0:
                  logFile.write(f"{ShipConversion[0]["name"]} ({ShipConversion[0]["hex_code"]}) received no items \n")
                else:
                  if len(altShipConversion)>0:
                    logFile.write(f"{altShipConversion[0]["name"]} ({altShipConversion[0]["hex_code"]}) received no items \n")
                  else:
                    logFile.write(f"{hex} received no items \n")
              else:
                for dest in shipLogs:
                  if stateVar==0:
                    #print(dest)
                    destTotals=sourceDict[hex][dest]
                    #print(destTotals)
                    srcShipConversion=shipNameLookup(hex)[0]
                    srcShipHex="{"+srcShipConversion["hex_code"]+"}"
                    srcShipConversion={"name":srcShipConversion["name"],"hex_code":srcShipHex}
                    #print(srcShipConversion)
                    if dest=="killed":
                      dstShipConversion={"name":"killed","hex_code":""}
                    elif "hurt" in dest:
                      dstShipConversion={"name":"hurt","hex_code":""}
                    else:
                      dstShipConversion=shipNameLookup(dest)[0]
                      dstShipHex="{"+dstShipConversion["hex_code"]+"}"
                      dstShipConversion={"name":dstShipConversion["name"],"hex_code":dstShipHex}
                  elif stateVar==1:
                    #print(f'dest=={dest}')
                    #print(f'hex=={hex}')
                    #print(f'sourceDict=={sourceDict}')
                    destTotals=sourceDict[hex][dest]
                    #print(destTotals)
                    if hex=="killed":
                      srcShipConversion={"name":hex,"hex_code":""}
                    else:
                      srcShipConversion=shipNameLookup(hex)[0]
                      srcShipHex="{"+srcShipConversion["hex_code"]+"}"
                      srcShipConversion={"name":srcShipConversion["name"],"hex_code":srcShipHex}
                    #print(srcShipConversion)
                    if dest=="killed":
                      dstShipConversion={"name":dest,"hex_code":""}
                    else:
                      try:
                        dstShipConversion=shipNameLookup(dest)[0]
                        dstShipHex="{"+dstShipConversion["hex_code"]+"}"
                        dstShipConversion={"name":dstShipConversion["name"],"hex_code":dstShipHex}
                      except:
                        dstShipConversion={"name":dest,"hex_code":""}
                  for item in destTotals:
                    itemCount = sourceDict[hex][dest][item]
                    if stateVar==0:
                      logFile.write(f"{srcShipConversion["name"]} {srcShipConversion["hex_code"]} sent {itemCount} {item} to {dstShipConversion["name"]} {dstShipConversion["hex_code"]} \n")
                    elif stateVar==1:
                      if srcShipConversion["name"] in NON_SHIP_ENTRIES or dstShipConversion["name"] in NON_SHIP_ENTRIES and configs[str(key)]["logFiltersNonShips"]:
                        #print("NON_SHIP_ENTITY")
                        pass
                      else:
                        logFile.write(f"{srcShipConversion["name"]} {srcShipConversion["hex_code"]} received {itemCount} {item} from {dstShipConversion["name"]} {dstShipConversion["hex_code"]} \n")
        writeToFile(shipTotals,"Transfer Send Logs",0)
        writeToFile(receiveTotals,"Transfer Receive Logs",1)
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
        def yesterday(frmt='%Y-%m-%d', string=True):
          return (datetime.now(pytz.UTC) - timedelta(days=1)).strftime('%Y-%m-%d')
        if year == None:
          message=f"{PlexusServer.name} Daily Transfer Report For {datetime.now(pytz.UTC)}"
        else:
          message=f"{PlexusServer.name} Daily Transfer Report For {int(year)}_{int(month)}_{int(day)}"
        await PlexusReportChannel.send(message,file=discord.File(log_file_name))
        os.remove(log_file_name)
    print("Plexus Daily Transfer Report Script Finished")
  
async def setup(bot: commands.Bot):
    await bot.add_cog(PlexusCmds(bot))

def individualLogs(log_file_name,route,findItemName,shipNameLookup):
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