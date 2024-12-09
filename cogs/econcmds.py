import os
import discord
from os import system
import time
import asyncio
import pytz
import sys
import datetime 
#import urllib2
import urllib.request
import requests
import gzip
from datetime import datetime, timedelta, timezone
from datetime import time as tme
#from keep_alive import keep_alive
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

DATE_GAP_CAP=30
SHIP_WEB_CAP=3

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

  def get_gzipped_json(url):
    return loads(gzip.decompress(requests.get(url).content))
  
  @commands.command(name="itemschema",help="This searches the item_schema.json file for the provided item_id Format: n!itemschema 1, ex: n!itemschema id 1 returns the entry for Iron because Iron's Item ID is 1.")
  async def itemschema(self,ctx,target_item):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      msgb = target_item #target_key + " " + target_item
      #lists.logback(ctx,msgb)
      url = "https://pub.drednot.io/test/econ/item_schema.json"
      response = loads(requests.get(url).content)
      def find_route(data, route_no):
        return list(filter(lambda x: x.get('id') == route_no, data))
      #if target_key == "name":
        #item = str(target_item)
      #elif target_key == "id":
        #item = int(target_item)
      #else:
        #await ctx.send("Target_key error")
      route = find_route(response,int(target_item))
      #embed=discord.Embed(title=f'{}', description=f'Clan Full Name: {route[0]["name"]}\nClan Abbreviation: {route[0]["abrv"]}\nClan Emoji: {route[0]["emoji"]}\nClan Relation: {route[0]["relation"]}', color=0xFF5733)
      #await ctx.send(embed=embed)
      await ctx.send(route)
    else:
      await ctx.send("I Had An Error Checking My Banned User List, Please Try Running The Command Again.")
      return False

  @commands.command(name="searchhexcode",hidden=False,aliases=['shex','hex','hexcode'],help="This searches either the ships or log file for all entries containing the provided HEX CODE!\n -Command Formart: n!searchhexcode <version> <year> <monthnumber> <day> <file (ships/log)> <hex_code (CASE SENSITVE)>.\n -The HEX CODE is a ships hex code in Dredark.\n -The EXTRA_KEY is for calling data from log.json, enter src or dst depending on if you want the source or destination, EXTRA_KEY is only if you pick the log file.\n -LOG_COUNT is for log.json only, it is how many items you want, as the logs could be upwards of 200+, in TEST SERVER the log can be 1,000+ items.")
  async def searchhexcode(self,ctx,version,year,mont,day,file,hex_code,extra_key="hex_code",log_count="none"):
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
      #print(route)
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

  @commands.command(name="detailedTransferSearch",hidden=False,aliases=['dts','dsearch','detailed'],disabled=False)
  async def detailedTransferSearch(self,ctx,version,startYear,startMonth,startDay,endYEar,endMonth,endDay,hex_code,extra_key="hex_code"):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      log_file_name=f"{hex_code}_{extra_key}_transfers.txt"
      logFile=None
      startDate=datetime(startYear,startMonth,startDay)
      endDate=datetime(endYEar,endMonth,endDay)
      delta=startDate-endDate
      if int(delta.days) > 30:
        return ctx.send(f"Sorry, the maximum amount of days that can be searched is `30`. You attempted to search `{int(delta.days)}` days. Your search was `{abs(delta-DATE_GAP_CAP)}` over the limit.")
      else:
        dates_to_scan=[]
        for i in range(delta.days + 1):
          day = start_date + timedelta(days=i)
          dates_to_scan.append(day)
        try:
          for date in dates_to_scan:
            splitDate=date.split("-")
            year=int(splitDate[0])
            month=int(splitDate[1])
            day=int(splitDate[2])
            jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/{version}/econ/{year}_{month}_{day}/log.json.gz')
            shipData = lists.get_gzipped_json(f'https://pub.drednot.io/{version}/econ/{year}_{month}_{day}/ships.json.gz')
            #if file == "log":
            hexcode="{"+hex_code+"}"
            def find_route(data, route_no):
              return list(filter(lambda x: x.get(extra_key) == route_no, data))
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
                logFile.write(f"Date (YYYY-MM-DD): {year}-{month}-{day}\n")
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
          message=f"Daily Transfer Report For Ship {hex_code}; Date: {datetime.now()}"
          await ctx.send(message,file=discord.File(log_file_name))
          os.remove(log_file_name)
    else:
      await ctx.send("Error")

  global tmes
  @tasks.loop(time=tmes)
  #@commands.command(name="ert")
  async def exchangeRatesUpdater(self):
    if self.bot.application_id==975858537223847936:
      print("Updating Exchange Rates")
      myguild = self.bot.get_guild(1031900634741473280)
      mychannel = await myguild.fetch_channel(1150474219021410357)
      threads=mychannel.threads
      year=datetime.today().year
      month=datetime.today().month
      day=datetime.today().day
      alldat = requests.get(f'https://pub.drednot.io/prod/econ/{int(year)}_{int(month)}_{(int(day)-1)}/summary.json').json()
      #alldat = requests.get(f'https://pub.drednot.io/prod/econ/2023_9_1/summary.json').json()
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
            #ib=float(datab[x])
            rate=(flux/item)*0.5
            divrate=(float(rate)*float(4))*0.5
            ratefinal="%.2f" % round(rate, 2)
            divfinal="%.5f" % round(divrate, 5)
            #rb=(flux/ib)*0.5
            #db=(float(rate)*float(16))*0.5
            #rbf="%.2f" % round(rb, 2)
            #dbf="%.2f" % round(db, 2)
            #avgrt=(float(ratefinal)+float(rbf))/float(2)
            #fxrt="%.2f" % round(avgrt, 2)
            #avgdv=(float(divfinal)+float(dbf))/float(2)
            #fxdv="%.2f" % round(avgdv, 2)
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
              #with requests.get(f"https://drednot.io/img/{itemname}", stream=True) as r:
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
              #print(len(f"Rate : `{ratefinal}`;\nDiv Rate : `{divfinal}`;\nName: `{itemname}`;\nId : `{int(x)}`;\nDate : `{datetime.today()}`\n\nChange:\n-Rate Change: `{ratechange}`\n-DivRate Change: `{divchange}`\nYesterday's Rates:\n-Yesterday's Rate: `{float(oldrate[1])}`\n-Yesterday's DivRate: `{float(olddiv[1])}`"))
              try:
                await thrd.send(f"Rate : `{ratefinal}`;\nDiv Rate : `{divfinal}`;\nName: `{itemname}`;\nId : `{int(x)}`;\nDate : `{datetime.today()}`\n\nChange:\n-Rate Change: `{ratechange}`\n-DivRate Change: `{divchange}`\n\nYesterday's Rates:\n-Yesterday's Rate: `{float(oldrate[1])}`\n-Yesterday's DivRate: `{float(olddiv[1])}`")
              except:
                print("Error")
        else:
          continue
      print("Exchange Rates Updated")

async def setup(bot: commands.Bot):
    await bot.add_cog(EconCmds(bot))
