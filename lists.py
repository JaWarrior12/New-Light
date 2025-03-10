import os
import discord
import time
import pytz
import datetime
import gzip
import requests
import aiohttp
import asyncio
#from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup

#Lists
authorized = [949451462151376948, 722703947638505556, 445763770799620097, 907899780561272842, 872718294023569408,930806975950909451]
banned = 0 #[948934984088035408,975761604975153233]
developers = [949451462151376948,722703947638505556,930284432634556496]
bgids=0

DEV_SERVER_ID = 1031900634741473280
#Authorized Based On Clan
#Self ID=974045822167679087


#CONSTANTS
NON_SHIP_ENTRIES=["Aqua Shielder","Red Sentry","Blue Rusher","The Shield Master","Shield Helper","Red Sniper",'Yellow Hunter',"The Lazer Enthusiast","The Coward","Orange Fool","Yellow Mine Guard","block - iron mine","bot - zombie tank","giant rubber ball","bot - zombie","block - vault","block - flux node","bot - zombie hunter","bot - zombie boss","block - treasure diamond"]


#Defs
def get_gzipped_json(url):
    return loads(gzip.decompress(requests.get(url).content))

async def get_gzipped_json_aiohttp(session,url):
  async with session.get(url) as response:
    file = await response.content.read()
    return loads(gzip.decompress(file))
  #return loads(gzip.decompress(session.get(url)))

def readFile(file):
  return loads(open(f'../NLDB/{file}.json', 'r').read())

def setFile(file,data):
    with open(f"../NLDB/{file}.json", "w") as f:
        f.write(dumps(data))

def getToken(id):
  data=loads(open('../NLDB/secrets.json', 'r').read())
  token=data[str(id)]
  print(token)
  return token

     
#Banned List
mylist = 0
def bannedlist():
  keyb=str("ban")
  global mylist
  mylist = dumps(readFile("config")[keyb])
  global banned
  banned = mylist

glist = 0
def bannedguilds():
  keyb=str("banguilds")
  global glist
  glist = dumps(readFile("config")[keyb])
  global bgids
  bgids = glist

def getguild(ctx):
  id = ctx.message.guild.id
  print(id)
  return id

def logback(ctx,msg):
  tz = pytz.timezone('America/New_York')
  ct = datetime.datetime.now(tz)
  usern = ctx.message.author.name
  userid = ctx.message.author.id
  commandrun = ctx.invoked_with
  mesg = msg
  guildid = getguild(ctx)
  guildn = ctx.message.guild.name
  #print(data)
  with open("Backups/log.txt", "a+") as g:
    g.write('\n')
    g.write(f'Command run at {ct}, by {usern} (User ID: {userid}), in server {guildn} (Server ID: {guildid}). Command Run: {commandrun}, Command Content: {mesg}')
    g.write('\n')
    
def logdown():
  tz = pytz.timezone('America/New_York')
  ct = datetime.datetime.now(tz)
  print("Disconnected")
  #print(data)
  with open("Backups/disconnectlogs.txt", "a+") as o:
    o.write('\n')
    o.write(f'New Light disconnected from the DISCORD platform at {ct}.')
    o.write('\n')
    
def clearserver(id):
  try:
    gid=str(id)
    data=readFile("distribution")
    if gid in data.keys():
      data.pop(gid)
      setFile("distribution",data)
    data=readFile("relations")
    if gid in data.keys():
      data.pop(gid)
      setFile("relations",data)
    data=readFile("quickping")
    if gid in data.keys():
      data.pop(gid)
      setFile("quickping",data)
    data=readFile("designs")
    if gid in data.keys():
      data.pop(gid)
      setFile("designs",data)
    data=readFile("config")
    if gid in data.keys():
      data.pop(gid)
      setFile("config",data)
    data=readFile("plexusSystems")
    if gid in data.keys():
      data.pop(gid)
      setFile("plexusSystems",data)
    data=readFile("other")
    if gid in data["defaultdist"].keys():
      data["defaultdist"].pop(gid)
      setFile("other",data)
    if gid in data["guild_IDs"].keys():
      data["guild_IDs"].pop(gid)
      setFile("other",data)
    if gid in data["cmdmetrics"].keys():
      data["cmdmetrics"].pop(gid)
      setFile("other",data)
  except:
    pass

async def logmajor(bot,ctx,msg):
  #Major Event Logging (To Channel In Developmnt Server)(Events Logged Are: Authorizing Users, Bans, Joins)
  tz = pytz.timezone('America/New_York')
  ct = datetime.datetime.now(tz)
  myguild = bot.get_guild(1031900634741473280)
  channel = myguild.get_channel(1037788623015268444)
  await channel.send(f'<@{930284432634556496}> !MAJOR EVENT! Command Run: {ctx.invoked_With}. Command Run At {ct} by {ctx.message.author.name} (User Id: {ctx.message.author.id}) in server {ctx.message.guild.name} (Server ID:{ctx.message.guild.id}. The Command Contained The Following Data: {msg}.')

def gidlist(self):
  data=readFile("other")
  for server in self.guilds:
    gn=str(server.name)
    gid=int(server.id)
    data["guild"].append({"name":gn,"id":gid})
  setFile("other",data)
    
    
    
def checkperms(ctx):
  #bannedlist()
  gid = str(ctx.message.guild.id)
  uid = str(ctx.message.author.id)
  keya="auth"
  autho = readFile("config")[gid]["auth"]
  if str(uid) not in banned:
    if str(uid) in autho:
      return True
    elif int(uid) in developers:
      return True
    elif str(uid) not in autho:
      return False
    else:
      return False
  elif str(uid) in banned:
    return False
  else:
    return False

def slashcheckperms(gidd,uidd):
  gid=str(gidd)
  uid=str(uidd)
  autho = readFile("config")[gid]["auth"]
  if str(uid) not in banned:
    if str(uid) in autho:
      return True
    elif int(uid) in developers:
      return True
    elif str(uid) not in autho:
      return False
    else:
      return False
  elif str(uid) in banned:
    return False
  else:
    return False

async def checkguild(bot,guild):
    myguild = bot.get_guild(1031900634741473280)
    mychannel = myguild.get_channel(1037788623015268444)
    invite = await guild.system_channel.create_invite(reason="Notifying My Developer That I Have Been Invited To A Server That Has Been Banned From Using Me")
    e = discord.Embed(title="Invited To Banned Server")
    e.add_field(name="Server Name", value=guild.name, inline=False)
    e.add_field(name="Invite Link", value=invite, inline=False)
    e.set_thumbnail(url=guild.icon)
    tz = pytz.timezone('America/New_York')
    e.timestamp=datetime.datetime.now(tz)
    await mychannel.send(embed=e)
    await mychannel.send(f'Guild Name: {guild}')
    await mychannel.send(f'Guild Id: {guild.id}')
    await guild.leave()

def lognewguild(stamp,msg,guild):
  with open("Backups/disconnectlogs.txt", "a+") as o:
      o.write(f'New Light {msg} {guild.name}, Id: {guild.id} at {stamp}.')
      o.write('\n\n')

def itemNameToID(item):
  formedbal=0
  #print(ship)
  #print(bal)
  url = "https://pub.drednot.io/test/econ/item_schema.json"
  #keys=list(ship.keys())
  #print(keys)
  #for x in keys:
  response = loads(requests.get(url).content)
  def find_route(data, route_no):
    return list(filter(lambda x: x.get('id') == route_no, data))
  #route = find_route(response,int(x))
  name="a"
  id=0
  #print(x)
  #FLux,Iron,Exp,Rubber,Ice,RC,Burst,Auto,Loader,Pusher,Scanner,Ball,HH
  i=item
  if str(i)=="iron":
    name="iron"
    id=1
  elif str(i)=="explosive":
    name="explosive"
    id=2
  elif str(i)=="rubber":
    name="rubber"
    id=4
  elif str(i)=="flux":
    name="flux"
    id=5
  elif str(i)=="handheld":
    name="handheld"
    id=104
  elif str(i)=="manifest_scanner":
    name="manifest_scanner"
    id=115
  elif str(i)=="bom_scanner":
    name="bom_scanner"
    id=116
  elif str(i)=="blueprint_scanner":
    name="blueprint_scanner"
    id=120
  elif str(i)=="pusher":
    name="pusher"
    id=242
  elif str(i)=="item_launcher":
    name="item_launcher"
    id=243
  elif str(i)=="rc" or str(i)=="cannon":
    name="cannon"
    id=226
  elif str(i)=="burst" or str(i)=="burst_cannon":
    name="burst_cannon"
    id=228
  elif str(i)=="auto" or str(i)=="machine" or str(i)=="machine_cannon":
    name="machine_cannon"
    id=229
  elif str(i)=="acute" or str(i)=="acute_cannon":
    name="acute_cannon"
    id=263
  elif str(i)=="msu" or str(i)=="munitions_supply_unit":
    name="munitions_supply_unit"
    id=264
  elif str(i)=="obtuse" or str(i)=="obtuse_cannon":
    name="obtuse_cannon"
    id=265
  elif str(i)=="loader":
    name="loader"
    id=252
  elif str(i)=="ice":
    name="ice"
    id=234
  elif str(i)=="volleyball":
    name="volleyball"
    id=51
  elif str(i)=="basketball":
    name="basketball"
    id=53
  elif str(i)=="beachball":
    name="beachball"
    id=55
  elif str(i)=="football":
    name="football"
    id=56
  elif str(i)=="rcd":
    name="rcd"
    id=122
  elif str(i)=="shield_generator":
    name="shield_generator"
    id=256
  elif str(i)=="shield_projector":
    name="shield_projector"
    id=257
  elif str(i)=="turret_controller":
    name="turret_controller"
    id=258
  elif str(i)=="rapid_booster":
    name="rapid_booster"
    id=162
  elif str(i)=="preservation_booster":
    name="preservation_boster"
    id=164
  elif str(i)=="shield_core":
    name="shield_core"
    id=123
  elif str(i)=="construction_gauntlets":
    name="construction_gauntlets"
    id=112
  elif str(i)=="hover_pack":
    name="hover_pack"
    id=114
  elif str(i)=="speed_skates":
    name="speed_skates"
    id=109
  elif str(i)=="booster_boots":
    name="booster_boots"
    id=110
  elif str(i)=="launcher_gauntlets":
    name="launcher_gauntlets"
    id=111
  elif str(i)=="rocket_pack":
    name="rocket_pack"
    id=113
  elif str(i)=="backpack":
    name="backpack"
    id=108
  else:
    id=0
  #print(formedbal)
  #print(oldbal)
  #print(formedbal)
  #print(f'ID: {id}')
  return id #dict(formedbal)

def formItem(ship):
    formedbal={}
    #response=bal
    #print(ship)
    #print(bal)
    url = "https://pub.drednot.io/test/econ/item_schema.json"
    keys=list(ship.keys())
    #print(keys)
    oldbal=0
  #for x in keys:
    def find_route(data, route_no):
      return list(filter(lambda x: x.get('item') == route_no, data))
    #route = find_route(response,int(x))
    route=ship["item"]
    print(route)
    name="a"
    print(ship["count"])
    i=route
    #FLux,Iron,Exp,Rubber,Ice,RC,Burst,Auto,Loader,Pusher,Scanner,Ball,HH
    if int(i)==1:
      name="iron"
      oldbal=oldbal+ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==2:
      name="explosive"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==4:
      name="rubber"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==5:
      name="flux"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==104:
      name="handheld"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==115:
      name="manifest_scanner"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==116:
      name="bom_scanner"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==120:
      name="blueprint_scanner"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==242:
      name="pusher"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==243:
      name="item_launcher"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==226:
      name="rc"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==228:
      name="burst"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==229:
      name="auto"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==252:
      name="loader"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==234:
      name="ice"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==51:
      name="volleyball"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==53:
      name="basketball"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==55:
      name="beachball"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==51:
      name="football"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==122:
      name="rcd"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==256:
      name="shield_generator"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==257:
      name="shield_projector"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==258:
      name="turret_controller"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==162:
      name="rapid_booster"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==164:
      name="preservation_boster"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==123:
      name="shield_core"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==112:
      name="construction_gauntlets"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==114:
      name="hover_pack"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==109:
      name="speed_skates"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==110:
      name="booster_boots"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==111:
      name="launcher_gauntlets"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==113:
      name="rocket_pack"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    elif int(i)==108:
      name="backpack"
      oldbal=ship["count"]
      formedbal.update({str(name):oldbal})
    else:
      asn=0
    #print(formedbal)
    #print(oldbal)
    print(formedbal)
    return dict(formedbal)

def itemNameById(item):
  url = "https://pub.drednot.io/test/econ/item_schema.json"
  response = loads(requests.get(url).content)
  def find_route(data, route_no):
      return list(filter(lambda x: x.get('id') == route_no, data))
  data=find_route(response,item)
  dat=data[0]
  return dat["name"]

def clrserver(id):
  gid=str(id)
  data=readFile("distribution")
  data.pop(gid)
  setFile("distribution",data)
  gid=str(id)
  data=readFile("relations")
  data.pop(gid)
  setFile("relations",data)
  gid=str(id)
  data=readFile("quickping")
  data.pop(gid)
  setFile("quickping",data)
  gid=str(id)
  data=readFile("designs")
  data.pop(gid)
  setFile("designs",data)
  gid=str(id)
  data=readFile("config")
  data.pop(gid)
  setFile("config",data)
  data=readFile("other")
  data["defaultdist"].pop(gid)
  setFile("other",data)