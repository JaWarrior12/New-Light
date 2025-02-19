import os
import discord
from os import system
import time
import asyncio
import aiohttp
import pytz
import sys
import datetime 
import urllib.request
import requests
import gzip
from datetime import datetime, timedelta, timezone
from datetime import time as tme
from discord.ext import commands, tasks
from discord.utils import get
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from json import loads, dumps
from backup import backup
from startup import startup

#Lists
import lists
#Auth For Leadership Commands
#authorized = lists.authorized
banned = lists.banned
developers = lists.developers


utc=timezone.utc
tmes=tme(hour=0,minute=30,tzinfo=utc)

# Max Run Time (MRT) Constants
MRT_BASE=5 # Minutes
MRT_MULTIPLIER=60 # Multiplier to get to proper unit. Scnds->Scnds is 1, Scnds->Mins is 60, Scnds->Hrs 3600 (NEVER USE THIS!!!!)
MAX_RUN_TIME=MRT_BASE*MRT_MULTIPLIER
MRT_UNIT="Minutes" # What Unit MAX_RUN_TIME Is In

DATE_GAP_CAP=365 # Original: 30
SHIP_WEB_CAP=3 # Original: 3

NON_SHIP_ENTRIES=lists.NON_SHIP_ENTRIES

class EconCmds(commands.Cog, name="Dredark Economy Dump Commands",description="All Commands relating to the Econ Dumps"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    if self.bot.user.id==975858537223847936:
      self.exchangeRatesUpdater.start()
  def cog_unload(self):
    if self.bot.user.id == 975858537223847936:
      self.exchangeRatesUpdater.cancel()
    else:
      pass

  def is_allowed():
    def predicate(ctx):
        return ctx.author.id in lists.developers #and ctx.guild.id in ALLOWED_SERVERS
    return commands.check(predicate)

  async def is_dm(ctx, arg):
    def predicate(ctx):
        return isinstance(ctx.channel, discord.channel.DMChannel)
    return commands.check(predicate)
  
  def get_gzipped_json(url):
    return loads(gzip.decompress(requests.get(url).content))
  
  @commands.command(name="itemschema",help="This searches the item_schema.json file for the provided item_id Format: n!itemschema 1, ex: n!itemschema id 1 returns the entry for Iron because Iron's Item ID is 1.")
  async def itemschema(self,ctx,target_item):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      msgb = target_item
      url = "https://pub.drednot.io/test/econ/item_schema.json"
      response = loads(requests.get(url).content)
      def find_route(data, route_no):
        return list(filter(lambda x: x.get('id') == route_no, data))
      route = find_route(response,int(target_item))
      await ctx.send(route)
    else:
      await ctx.send("I Had An Error Checking My Banned User List, Please Try Running The Command Again.")
      return False

  @commands.command(name="searchhexcode",hidden=False,aliases=['shex','hex','hexcode'],help="Note: If you want a transfer log, use `detailedTransferSearch`. This searches either the ships or log file for all entries containing the provided HEX CODE!\n -Command Formart: n!searchhexcode <version> <year> <monthnumber> <day> <file (ships/log)> <hex_code (CASE SENSITVE)>.\n -The HEX CODE is a ships hex code in Dredark.\n -The EXTRA_KEY is for calling data from log.json, enter src or dst depending on if you want the source or destination, EXTRA_KEY is only if you pick the log file.\n -LOG_COUNT is for log.json only, it is how many items you want, as the logs could be upwards of 200+, in TEST SERVER the log can be 1,000+ items.")
  async def searchhexcode(self,ctx,version,year,month,day,file,hex_code,extra_key="hex_code",log_count="none"):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/{version}/econ/{year}_{month}_{day}/{file}.json.gz')
      if file == "log":
        hexcode="{"+hex_code+"}"
      else:
        hexcode=hex_code
      def find_route(data, route_no):
        return list(filter(lambda x: x.get(extra_key) == route_no, data))
      route = find_route(jsondata,hexcode)
      if len(route) <= 10:
        await ctx.send(route)
      else:
        await ctx.send(f'The length of the list I want to give you is too long to send in discord as one message. There are {len(route)} items and I can only send lists of less than or equal to 10 items (Discord Character Limit). I will now send the list in chunks of ~10ish. Amount of items sent is based on the LOG_COUNT key.')
        i=0
        if log_count == "none":
          log_count=100
        else:
          pass
        b=int(log_count)
        for x in route:
          routeb=route[i:i+9]
          await ctx.send("----------")
          await ctx.send(routeb)
          i=i+10
          if int(i) >= int(b):
            break
          elif int(i) == int(b):
            break
          elif int(i) <= int(b):
            continue
          else:
            break
    else:
      await ctx.send("Error")

  @commands.command(name="detailedTransferSearch",help="This command returns all source/destination transfers from a given ship between provided dates. Filter Options: normal (only ships), all (Includes bots/terrain)",hidden=False,aliases=['dts','dsearch','detailed'],disabled=False)
  @commands.cooldown(5, 60, commands.BucketType.default)
  async def detailedTransferSearch(self,ctx,version,startYear,startMonth,startDay,endYear,endMonth,endDay,hex_code,filterVal="normal"):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      startTime=time.time()
      log_file_name=f"{hex_code}_transfers.txt"
      logFile=None
      itemInfo={}
      startDate=datetime(int(startYear),int(startMonth),int(startDay))
      endDate=datetime(int(endYear),int(endMonth),int(endDay))
      delta=endDate-startDate
      if int(delta.days) > DATE_GAP_CAP:
        return ctx.send(f"Sorry, the maximum amount of days that can be searched is `{DATE_GAP_CAP}`. You attempted to search `{int(delta.days)}` days. Your search was `{abs(delta-DATE_GAP_CAP)}` over the limit.")
      else:
        await ctx.send("Collecting Data! This may take a minute or so...")
        dates_to_scan=[]
        for i in range(delta.days + 1):
          day = startDate + timedelta(days=i)
          dates_to_scan.append(day)
        try:
          hexcode="{"+hex_code+"}"
          shipTotals={}
          receiveTotals={}
          shipNames={}
          currRunTime=abs(time.time()-startTime)
          for date in dates_to_scan:
            if currRunTime > MAX_RUN_TIME:
              await ctx.send(f"Sorry, There Is A MAX RUN TIME of {MAX_RUN_TIME} {MRT_UNIT}(s). This Run has exceeded that limity by {abs(currRunTime-MAX_RUN_TIME)} {MRT_UNIT}(s). Please tyr again with a shorter search range.")
              await ctx.send("Search Ended. Search Results Will be Sent Incomplete.")
              break
            year=int(date.year)
            month=int(date.month)
            day=int(date.day)
            try:
              async with aiohttp.ClientSession() as session:
                jsondata = await lists.get_gzipped_json_aiohttp(session,f'https://pub.drednot.io/{version}/econ/{year}_{month}_{day}/log.json.gz')
                shipData = await lists.get_gzipped_json_aiohttp(session,f'https://pub.drednot.io/{version}/econ/{year}_{month}_{day}/ships.json.gz')
                altShipData = await lists.get_gzipped_json_aiohttp(session,f'https://pub.drednot.io/prod/econ/{int(year)}_{int(month)}_{int(day)}/ships.json.gz')
            except gzip.BadGzipFile:
              continue
            oldHexcode=hex_code
            shipTotals.update({oldHexcode:{}})
            receiveTotals.update({oldHexcode:{}})
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
            sourceHurtItems={}
            #Logs A,B,C Are For Sending
            for logA in route:
              destShip=logA["dst"].replace("{","").replace("}","")
              if destShip not in list(items.keys()):
                items.update({destShip:{}})
            for logB in route:
              destShip=logB["dst"].replace("{","").replace("}","")
              itemName=str(findItemName(logB["item"])[0]["name"])
              items.update({destShip:{str(itemName):0}})
            for logC in route:
              destShip=logC["dst"].replace("{","").replace("}","")
              itemName=findItemName(logC["item"])[0]["name"]
              itemList=list(items[destShip].keys())
              if itemName not in itemList:
                items[destShip].update({str(itemName):0})
              items[destShip][str(itemName)]+=logC["count"]

            #Logs D,E,F Are For Receiving Logs
            for logD in destList:
              destShip=logD["src"].replace("{","").replace("}","")
              if destShip not in list(destItems.keys()):
                destItems.update({destShip:{}})
            for logE in destList:
              destShip=logE["src"].replace("{","").replace("}","")
              itemName=str(findItemName(logE["item"])[0]["name"])
              destItems.update({destShip:{str(itemName):0}})
            for logF in destList:
              destShip=logF["src"].replace("{","").replace("}","")
              itemName=findItemName(logF["item"])[0]["name"]
              if itemName not in list(destItems[destShip].keys()):
                destItems[destShip].update({str(itemName):0})
              destItems[destShip][str(itemName)]+=logF["count"]
            shipTotals.update({oldHexcode:items})
            receiveTotals.update({oldHexcode:destItems})
            def writeToFile(sourceDict,sectionTitle,stateVar):
              #StateVar is 1 or 2. 1==Send/shipTotals, 2==Receive/receiveTotals
              with open(log_file_name, "a+", encoding="utf-8") as logFile:
                if sum(1 for _ in logFile)==0:
                  logFile.write(f"--\\/--{sectionTitle}--\\/--\n")
                else:
                  logFile.write(f"\n\n--\\/--{sectionTitle}--\\/--\n")
                shipTotalsKeys=list(sourceDict.keys())
                for hex in shipTotalsKeys:
                  shipLogs=sourceDict[hex]
                  if len(list(sourceDict[hex].keys()))==0 and stateVar==1:
                    hexCode=hex
                    ShipConversion=shipNameLookup(hexCode)
                    altShipConversion=altShipNameLookup(hexCode)
                    if len(ShipConversion)>0:
                      logFile.write(f"{ShipConversion[0]["name"]} ({ShipConversion[0]["hex_code"]}) transfered no items \n")
                    else:
                      if len(altShipConversion)>0:
                        logFile.write(f"{altShipConversion[0]["name"]} ({altShipConversion[0]["hex_code"]}) transfered no items \n")
                      else:
                        logFile.write(f"{hex} transfered no items \n")
                  elif len(list(sourceDict[hex].keys()))==0 and stateVar==2:
                    hexCode=hex
                    ShipConversion=shipNameLookup(hexCode)
                    altShipConversion=altShipNameLookup(hexCode)
                    if len(ShipConversion)>0:
                      logFile.write(f"{ShipConversion[0]["hex_code"]} ({ShipConversion[0]["hex_code"]}) received no items \n")
                      if ShipConversion[0]["hex_code"] not in list(shipNames.keys()):
                        shipNames.update({ShipConversion[0]["hex_code"]:[ShipConversion[0]["name"]]})
                      elif ShipConversion[0]["hex_code"] in list(shipNames.keys()):
                        if ShipConversion[0]["name"] not in shipNames[ShipConversion[0]["hex_code"]]:
                          shipNames[ShipConversion[0]["hex_code"]].append(ShipConversion[0]["name"])
                    else:
                      if len(altShipConversion)>0:
                        logFile.write(f"{altShipConversion[0]["name"]} ({altShipConversion[0]["hex_code"]}) received no items \n")
                        if altShipConversion[0]["hex_code"] not in list(shipNames.keys()):
                          shipNames.update({altShipConversion[0]["hex_code"]:[altShipConversion[0]["name"]]})
                        elif altShipConversion[0]["hex_code"] in list(shipNames.keys()):
                          if altShipConversion[0]["name"] not in shipNames[altShipConversion[0]["hex_code"]]:
                            shipNames[altShipConversion[0]["hex_code"]].append(altShipConversion[0]["name"])
                      else:
                        logFile.write(f"{hex} received no items \n")
                  else:
                    for dest in shipLogs:
                      if stateVar==1:
                        destTotals=sourceDict[hex][dest]
                        srcShipConversion=shipNameLookup(hex)[0]
                        srcShipHex="{"+srcShipConversion["hex_code"]+"}"
                        srcShipName=srcShipConversion["name"]
                        if "hurt" in srcShipConversion["name"]:
                          srcShipConversion={"name":srcShipName,"hex_code":""}
                        else:
                          srcShipConversion={"name":srcShipConversion["name"],"hex_code":srcShipHex}
                        if dest=="killed":
                          dstShipConversion={"name":"killed","hex_code":""}
                        elif "hurt" in dest:
                          dstShipConversion=shipNameLookup(dest)[0]
                          dstShipHex="{"+dstShipConversion["hex_code"]+"}"
                          if dstShipHex == hexcode:
                            continue
                          else:
                            dstShipConversion=shipNameLookup(dest)[0]
                            dstShipConversion={"name":f'{dstShipConversion["name"]}',"hex_code":""}
                        else:
                          dstShipConversion=shipNameLookup(dest)[0]
                          dstShipHex="{"+dstShipConversion["hex_code"]+"}"
                          dstShipConversion={"name":dstShipConversion["name"],"hex_code":dstShipHex}
                      elif stateVar==2:
                        destTotals=sourceDict[hex][dest]
                        if hex=="killed":
                          srcShipConversion={"name":hex,"hex_code":""}
                        else:
                          srcShipConversion=shipNameLookup(hex)[0]
                          srcShipHex="{"+srcShipConversion["hex_code"]+"}"
                          srcShipConversion={"name":srcShipConversion["name"],"hex_code":srcShipHex}
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
                        if stateVar==1:
                          logFile.write(f"{srcShipConversion["name"]} {srcShipConversion["hex_code"]} sent {itemCount} {item} to {dstShipConversion["name"]} {dstShipConversion["hex_code"]} \n")
                          if srcShipConversion["hex_code"] not in list(shipNames.keys()):
                            shipNames.update({srcShipConversion["hex_code"]:[srcShipConversion["name"]]})
                          elif srcShipConversion["hex_code"] in list(shipNames.keys()):
                            if srcShipConversion["name"] not in shipNames[srcShipConversion["hex_code"]]:
                              shipNames[srcShipConversion["hex_code"]].append(srcShipConversion["name"])
                        elif stateVar==2:
                          if (srcShipConversion["name"] in NON_SHIP_ENTRIES or dstShipConversion["name"] in NON_SHIP_ENTRIES):
                            if filterVal == "all":
                              pass
                            elif filterVal == "normal":
                              pass
                          else:
                            logFile.write(f"{srcShipConversion["name"]} {srcShipConversion["hex_code"]} received {itemCount} {item} from {dstShipConversion["name"]} {dstShipConversion["hex_code"]} \n")
                            if srcShipConversion["hex_code"] not in list(shipNames.keys()):
                              shipNames.update({srcShipConversion["hex_code"]:[srcShipConversion["name"]]})
                            elif srcShipConversion["hex_code"] in list(shipNames.keys()):
                              if srcShipConversion["name"] not in shipNames[srcShipConversion["hex_code"]]:
                                shipNames[srcShipConversion["hex_code"]].append(srcShipConversion["name"])
            with open(log_file_name, "a", encoding="utf-8") as logFile:
              logFile.write(f"\nDate (YYYY-MM-DD): {year}-{month}-{day}\n")
            writeToFile(shipTotals,"Transfer Send Logs",1)
            writeToFile(receiveTotals,"Transfer Receive Logs",2)
        except Exception as e:
          await ctx.send(f"Error: {e}")
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
        with open(log_file_name, "a", encoding="utf-8") as logFile:
            for ship in list(shipNames.keys()):
              if len(shipNames[ship])>0:
                logFile.write(f"\n- Names Used By {shipNames[ship][-1]} ({ship}) During Search Range: {shipNames[ship]}")
        if logFile != None:
          message=f"Historic Transfer Report For Ship {hex_code}; Start Date: {startDate}, End Date: {endDate}; Period: {delta}"
          await ctx.send(message,file=discord.File(log_file_name))
          os.remove(log_file_name)
    else:
      await ctx.send("Error")

  @commands.command(name="readShiplist",aliases=["rsl"],help="This command reads the shiplist file provided and returns a formatted list of all ships that are owned and/or cap on.",hidden=True)
  @commands.check_any(is_allowed())
  async def readShiplist(self,ctx,onlyOwned="True",saveList="False",userDiscordID=None,*,username=None):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      if username==None:
        return await ctx.send("Please Provide The Username Attached To The Shiplist.")
      if userDiscordID==None:
        return await ctx.send("Please Provide The Discord ID Of The User.")
      log_file_name=f"{username}_shiplist.txt"
      logFile=None
      if len(ctx.message.attachments) >=1:
        shiplist_file=ctx.message.attachments[0]
        ownedShips={}
        cappedShips={}
        listData=await shiplist_file.read()
        ships=loads(listData)["ships"]
        for hex in ships.items():
          ship=hex[1]
          if ship["owned"]==True:
            ownedShips.update({ship["hex_code"]:ship})
          if (ship["saved"]==True and ship["owned"]==False) and onlyOwned.lower() in ["false","no","off","0","False"]:
            cappedShips.update({ship["hex_code"]:ship})
        with open(log_file_name, "a", encoding="utf-8") as logFile:
          if len(ownedShips)>0:
            logFile.write(f"--\\/--Owned Ships--\\/--\n")
            for ship in ownedShips.items():
              ship=ship[1]
              logFile.write(f" - {ship['team_name']} ({ship['hex_code']})\n")
          if len(cappedShips)>0 and onlyOwned.lower() in ["false","no","off","0","False"]:
            logFile.write(f"\n\n--\\/--Captain On Ships--\\/--\n")
            for ship in cappedShips.items():
              ship=ship[1]
              logFile.write(f" - {ship['team_name']} ({ship['hex_code']})\n")
        if logFile != None:
          message=f"Ship List For {username}"
          await ctx.send(message,file=discord.File(log_file_name))
          os.remove(log_file_name)
        try:
          if saveList.lower() in["true","yes","on","1","True"]:
            data=lists.readFile("shipLists")
            if username not in list(data["users"].keys()):
              data["users"].update({username:{"discordID":userDiscordID,"whitelist":[],"owned":ownedShips,"capped":cappedShips}})
            else:
              for ship in ownedShips.items():
                if ship not in list(data["users"][username]["owned"].items()):
                  ship=ship[1]
                  data["users"][username]["owned"].update({ship["hex_code"]:ship})
              for ship in cappedShips.items():
                if ship not in list(data["users"][username]["capped"].items()):
                  ship=ship[1]
                  data["users"][username]["capped"].update({ship["hex_code"]:ship})
            lists.setFile("shipLists",data)
        except Exception as e:
          print(e)
      else:
        await ctx.send("Please Attach A File To Read.")
    else:
      await ctx.send("Error")

  @commands.command(name="submitShipList",aliases=["ssl"],help="Allows a user to submit their ship list privately, and whitelist who can use it.",hidden=True)
  @commands.check_any(is_allowed())
  async def submitShipList(self,ctx,onlyOwned="True",*,whitelist):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      username=ctx.message.author.name
      userDiscordID=ctx.message.author.id
      realWhitelist=[]
      for item in whitelist.split(","):
        item=item.strip(" ")
        realWhitelist.append(item)
      log_file_name=f"{username}_shiplist.txt"
      logFile=None
      if len(ctx.message.attachments) >=1:
        shiplist_file=ctx.message.attachments[0]
        ownedShips={}
        cappedShips={}
        listData=await shiplist_file.read()
        ships=loads(listData)["ships"]
        for hex in ships.items():
          ship=hex[1]
          if ship["owned"]==True:
            ownedShips.update({ship["hex_code"]:ship})
          if (ship["saved"]==True and ship["owned"]==False) and onlyOwned.lower() in ["false","no","off","0","False"]:
            cappedShips.update({ship["hex_code"]:ship})
        with open(log_file_name, "a", encoding="utf-8") as logFile:
          if len(ownedShips)>0:
            logFile.write(f"--\\/--Owned Ships--\\/--\n")
            for ship in ownedShips.items():
              ship=ship[1]
              logFile.write(f" - {ship['team_name']} ({ship['hex_code']})\n")
          if len(cappedShips)>0 and onlyOwned.lower() in ["false","no","off","0","False"]:
            logFile.write(f"\n\n--\\/--Captain On Ships--\\/--\n")
            for ship in cappedShips.items():
              ship=ship[1]
              logFile.write(f" - {ship['team_name']} ({ship['hex_code']})\n")
        if logFile != None:
          message=f"Ship List For {username}"
          await ctx.send(message,file=discord.File(log_file_name))
          os.remove(log_file_name)
        try:
          data=lists.readFile("shipLists")
          if username not in list(data["users"].keys()):
            data["users"].update({username:{"discordID":userDiscordID,"whitelist":[],"owned":ownedShips,"capped":cappedShips}})
          else:
            for ship in ownedShips.items():
              if ship not in list(data["users"][username]["owned"].items()):
                ship=ship[1]
                data["users"][username]["owned"].update({ship["hex_code"]:ship})
            for ship in cappedShips.items():
              if ship not in list(data["users"][username]["capped"].items()):
                ship=ship[1]
                data["users"][username]["capped"].update({ship["hex_code"]:ship})
          data["users"][username]["whitelist"]=realWhitelist
          lists.setFile("shipLists",data)
        except Exception as e:
          print(e)
      else:
        await ctx.send("Please Attach A File To Read.")
    else:
      await ctx.send("Error")

  global tmes
  @tasks.loop(time=tmes)
  async def exchangeRatesUpdater(self):
    if self.bot.application_id==975858537223847936:
      print("Updating Exchange Rates")
      myguild = self.bot.get_guild(1031900634741473280)
      mychannel = await myguild.fetch_channel(1150474219021410357)
      threads=mychannel.threads
      year=datetime.today().year
      month=datetime.today().month
      day=datetime.today().day
      async with aiohttp.ClientSession() as session:
        alldat = await session.get(f'https://pub.drednot.io/prod/econ/{int(year)}_{int(month)}_{(int(day)-1)}/summary.json').json()
      data=alldat["items_held"]
      datab=alldat["items_moved"]
      keys=list(data.keys())
      flux=float(data["5"])
      tracked=[1,2,3,4,5,51,53,55,56,102,104,108,109,110,111,112,113,114,115,116,120,122,123,162,164,226,228,229,263,264,265,234,242,243,246,252,253,256,257,258,305,306,307]
      for x in keys:
        if int(x) in tracked:
          if x == "5":
            continue
          else:
            item=float(data[x])
            rate=(flux/item)*0.5
            divrate=(float(rate)*float(4))*0.5
            ratefinal="%.2f" % round(rate, 2)
            divfinal="%.5f" % round(divrate, 5)
            itemname=lists.itemNameById(int(x))
            def find_route(lst, route_no):
              found=[]
              for z in lst:
                if z.name==route_no:
                  found.append(z)
              return found
            thd=find_route(threads,itemname)
            if len(thd)==0:
              await mychannel.create_thread(name=itemname,content=f'Exchange Rate For {itemname}')
              await asyncio.sleep(0.1)
              upmc=await myguild.fetch_channel(1150474219021410357)
              newthread=upmc.get_thread(upmc.last_message_id)
              await newthread.send(content=f"Rate : `{ratefinal}`;\nDivRate : `{divfinal}`;\nName: `{itemname}`;\nId : `{int(x)}`;\nDate : `{datetime.today()}`")
            else:
              thrd=mychannel.get_thread(thd[0].id)
              cm = [message async for message in thrd.history(limit=2)]
              cntnt=cm[0].content
              cntnt=cntnt.replace("`","").replace("\n","")
              ctnt=cntnt.split(";")
              oldrate=(ctnt[0].split(":"))
              olddiv=(ctnt[1].split(":"))
              ratechange=float(ratefinal)-float(oldrate[1])
              divchange=float(divfinal)-float(olddiv[1])
              await thrd.purge(limit=1)
              try:
                await thrd.send(f"Rate : `{ratefinal}`;\nDiv Rate : `{divfinal}`;\nName: `{itemname}`;\nId : `{int(x)}`;\nDate : `{datetime.today()}`\n\nChange:\n-Rate Change: `{ratechange}`\n-DivRate Change: `{divchange}`\n\nYesterday's Rates:\n-Yesterday's Rate: `{float(oldrate[1])}`\n-Yesterday's DivRate: `{float(olddiv[1])}`")
              except:
                print("Error")
        else:
          continue
      print("Exchange Rates Updated")

async def setup(bot: commands.Bot):
    await bot.add_cog(EconCmds(bot))
