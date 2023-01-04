import os, discord
from os import system
import time
import pytz
import datetime 
#import urllib2
import urllib.request
import requests
import gzip
#from keep_alive import keep_alive
from discord.ext import commands
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
#Authorized Based On Clan
nlcauth = lists.nlcauth
bocauth = lists.bocauth
dsrauth = lists.dsrauth
tsauth = lists.tsauth
ffauth = lists.ffauth
#Server IDs
NLC = lists.NLC
BOC = lists.BOC
TestSrvr = lists.TestSrvr
DSR = lists.DSR
FRF = lists.FRF

class EconCmds(commands.Cog, name="Dredark Economy Dump Commands",description="All Commands relating to the Econ Dumps"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  def get_gzipped_json(url):
    return loads(gzip.decompress(requests.get(url).content))
  
  @commands.command(name='readecon',brief='Test Command for devs.',hidden=True,help="Testing Command For Dredark Econ Data Dumps!")
  @commands.has_role('Developer')
  async def econdump(self,ctx,msg):
    #msgparts, datax = msg.split(" ")
    await ctx.send("Hi")
    #response = requests.get("https://pub.drednot.io/test/econ/2022_11_13/log.json.gz")#,params={'q': 'requests+language:python'})
    #data = response.content
    #json_response = response.json()
    #repository = json_response[0]
    #await ctx.send(repository)
    #with gzip.open(data, 'rb') as f:
      #file_content = f.read(33)
      #json_resb = file_content.json
      #repository = json_resb[0 
    jsondata = lists.get_gzipped_json("https://pub.drednot.io/test/econ/2022_11_18/log.json.gz")
    await ctx.send(len(jsondata))
    await ctx.send(jsondata[int(msg)])
    #for i, line in enumerate(data.split('\n')):
      #await ctx.send(f'{i}   {line}')

  @commands.command(name="econitemsnew",help="This will call from the Dredark Public Economy Data Dumps. This command only handles the items_new key. \n -Command Format: n!econdata VERSION YEAR MONTHNUMBER DAY KEYS; \n-VERSION is test or prod (main server); \n-The DATE formating for November 13th, 2022 is as follows: n!econdata 2022 11 13; \n-KEY FORMATING: The key you input is for what item will be called from, this is a value from 0->30; \n-Formatting Keys: To format search keys you must use data provided by Cogg at https://drednot.io/c/coder-docs in the Econ Dumps item;",aliases=['ecin','ecnewitems','eitemsnew'])
  async def econitemsnew(self,ctx,version,year,monthnumber,day,keys):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
      return False
    elif str(ctx.message.author.id) not in banned:
      msgb = version + " " + year + " " + monthnumber  + " " + day + " " + keys
      lists.logback(ctx,msgb)
      #keyparts, datax = keys.split(" ")
      response = requests.get(f'https://pub.drednot.io/{version}/econ/{int(year)}_{int(monthnumber)}_{int(day)}/summary.json',params={'q': 'requests+language:python'})
      json_response = response.json()
      repository = json_response["items_new"][int(keys)]
      await ctx.send(repository)
    else:
      await ctx.send("I Had An Error Checking My Banned User List, Please Try Running The Command Again.")
      return False

  @commands.command(name="itemschema",help="This searches the item_schema.json file for the provided item_id Format: n!itemschema 1, ex: n!itemschema id 1 returns the entry for Iron because Iron's Item ID is 1.")
  async def itemschema(self,ctx,target_item):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      msgb = target_item #target_key + " " + target_item
      lists.logback(ctx,msgb)
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

  @commands.command(name="econdata",help="Calls data from one of the following keys: count_ships/count_logs/items_held/items_moved")
  async def econdata(self,ctx,version,year,monthnumber,day,key):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      msgb = version + " " + year + " " + monthnumber  + " " + day + " " + key
      lists.logback(ctx,msgb)
      response = requests.get(f'https://pub.drednot.io/{version}/econ/{int(year)}_{int(monthnumber)}_{int(day)}/summary.json',params={'q': 'requests+language:python'})
      json_response = response.json()
      repository = json_response[key]
      await ctx.send(repository)
    else:
      await ctx.send("I Had An Error Checking My Banned User List, Please Try Running The Command Again.")
      return False

  @commands.command(name="readlogs",help="Reads the log file from the Dred Public Econ Dumps. \nFormatting:\n -Version is test or prod(main server)\n -Year,MonthNumber,Day follow date formatting (2022_11(month,november)_13(day)\n -Key is a number 1-50000 to start (acutal max will be provided once yiu run the command so you can run again with real data.")
  async def readligs(self,ctx,version,year,monthnumber,day,key):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      msgb = version + " " + year + " " + monthnumber  + " " + day + " " + key
      lists.logback(ctx,msgb)
      jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/{version}/econ/{year}_{monthnumber}_{day}/log.json.gz')
      await ctx.send(len(jsondata))
      await ctx.send(jsondata[int(key)])
    else:
      await ctx.send("Error")

  @commands.command(name="readships",help="Reads the ships file from the Dred Public Econ Dumps. \nFormatting:\n -Version is test or prod(main server)\n -Year,MonthNumber,Day follow date formatting (2022_11(month,november)_13(day)\n -Key is a number 1-50000 to start (acutal max will be provided once yiu run the command so you can run again with real data.")
  async def readships(self,ctx,version,year,monthnumber,day,key):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      msgb = version + " " + year + " " + monthnumber  + " " + day + " " + key
      lists.logback(ctx,msgb)
      jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/{version}/econ/{year}_{monthnumber}_{day}/ships.json.gz')
      await ctx.send(len(jsondata))
      await ctx.send(jsondata[int(key)])
    else:
      await ctx.send("Error")

  @commands.command(name="searchhexcode",hidden=False,aliases=['shex','hex','hexcode'],help="This searches either the ships or log file for all entries containing the provided HEX CODE!\n -Command Formart: n!searchhexcode <version> <year> <monthnumber> <day> <file (ships/log)> <hex_code (CASE SENSITVE)>.\n -The HEX CODE is a ships hex code in Dredark.\n -The EXTRA_KEY is for calling data from log.json, enter src or dst depending on if you want the source or destination, EXTRA_KEY is only if you pick the log file.\n -LOG_COUNT is for log.json only, it is how many items you want, as the logs could be upwards of 200+, in TEST SERVER the log can be 1,000+ items.")
  async def writeconfile(self,ctx,version,year,month,day,file,hex_code,extra_key="hex_code",log_count="none"):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    elif str(ctx.message.author.id) not in banned:
      msgb = version + " " + year + " " + month  + " " + day + " " + file + " " + hex_code +" "+ extra_key+" "+log_count
      lists.logback(ctx,msgb)
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
  

async def setup(bot: commands.Bot):
    await bot.add_cog(EconCmds(bot))