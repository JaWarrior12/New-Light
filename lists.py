import os, discord
import time
import pytz
import datetime
import gzip
import requests
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

#Authorized Based On Clan
#Self ID=974045822167679087
nlcauth = [949451462151376948,445763770799620097]
bocauth = [949451462151376948,907899780561272842]
dsrauth = [949451462151376948,872718294023569408]
tsauth = [949451462151376948,722703947638505556]
ffauth = [949451462151376948,930806975950909451]

#Server IDs
NLC = 754778020639932516
BOC = 966067610779271168
TestSrvr = 975858783504969808
DSR = 872725039097720883
FRF = 952133314137956362
BotDevelopmentServer=1031900634741473280

#Defs
def readdata():
    return loads(open('../NLDB/distribution.json', 'r').read())

def setdata(data):
    with open("../NLDB/distribution.json", "w") as f:
        f.write(dumps(data))

def readdataB():
    return loads(open("../NLDB/relations.json","r").read())

def setdataB(dataB):
    with open("../NLDB/relations.json", "w") as g:
        g.write(dumps(dataB))

def readdataC():
    return loads(open('../NLDB/quickping.json', 'r').read())

def setdataC(dataC):
    with open("../NLDB/quickping.json", "w") as g:
        g.write(dumps(dataC))

def readdataD():
    return loads(open('../NLDB/designs.json', 'r').read())

def setdataD(dataD):
    with open("../NLDB/designs.json", "w") as g:
        g.write(dumps(dataD))
      
def readdataE():
    return loads(open('../NLDB/config.json', 'r').read())

def setdataE(datae):
    with open("../NLDB/config.json", "w") as h:
        h.write(dumps(datae))

def readother():
    return loads(open('../NLDB/other.json', 'r').read())

def setother(datah):
    with open("../NLDB/other.json", "w") as f:
        f.write(dumps(datah))

def bals():
    return loads(open('../NLDB/distribution.json', 'r').read())

def get_gzipped_json(url):
    return loads(gzip.decompress(requests.get(url).content))

     
#Banned List
mylist = 0
def bannedlist():
  keyb=str("ban")
  global mylist
  mylist = dumps(readdataE()[keyb])
  global banned
  banned = mylist

glist = 0
def bannedguilds():
  keyb=str("banguilds")
  global glist
  glist = dumps(readdataE()[keyb])
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
    data=readdata()
    data.pop(gid)
    setdata(data)
    gid=str(id)
    data=readdataB()
    data.pop(gid)
    setdataB(data)
    gid=str(id)
    data=readdataC()
    data.pop(gid)
    setdataC(data)
    gid=str(id)
    data=readdataD()
    data.pop(gid)
    setdataD(data)
    gid=str(id)
    data=readdataE()
    data.pop(gid)
    setdataE(data)
    data=readother()
    data["defaultdist"].pop(gid)
    setother(data)
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
  data=readother()
  for server in self.guilds:
    gn=str(server.name)
    gid=int(server.id)
    data["guild"].append({"name":gn,"id":gid})
  setother(data)
    
    
    
def checkperms(ctx):
  #bannedlist()
  gid = str(ctx.message.guild.id)
  uid = str(ctx.message.author.id)
  keya="auth"
  autho = readdataE()[gid]["auth"]
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
  autho = readdataE()[gid]["auth"]
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
    await guild.leave

def lognewguild(stamp,msg,guild):
  with open("Backups/disconnectlogs.txt", "a+") as o:
      o.write(f'New Light {msg} {guild.name}, Id: {guild.id} at {stamp}.')
      o.write('\n\n')

def formatClanBal(ship,bal):
  formedbal={}
  #print(ship)
  #print(bal)
  url = "https://pub.drednot.io/test/econ/item_schema.json"
  keys=list(ship.keys())
  #print(keys)
  for x in keys:
    response = loads(requests.get(url).content)
    def find_route(data, route_no):
      return list(filter(lambda x: x.get('id') == route_no, data))
    #route = find_route(response,int(x))
    name="a"
    #print(x)
    #FLux,Iron,Exp,Rubber,Ice,RC,Burst,Auto,Loader,Pusher,Scanner,Ball,HH
    if int(x)==1:
      name="iron"
      oldbal=ship["1"]
      formedbal.update({str(name):oldbal})
    elif int(x)==2:
      name="explosive"
      oldbal=ship["2"]
      formedbal.update({str(name):oldbal})
    elif int(x)==4:
      name="rubber"
      oldbal=ship["4"]
      formedbal.update({str(name):oldbal})
    elif int(x)==5:
      name="flux"
      oldbal=ship["5"]
      formedbal.update({str(name):oldbal})
    elif int(x)==104:
      name="hhs"
      oldbal=ship["104"]
      formedbal.update({str(name):oldbal})
    elif int(x)==115 or int(x)==116 or int(x)==120:
      name="scanners"
      old=formedbal[name]
      oldbal=ship[x]
      newbal=int(oldbal)+int(old)
      formedbal.update({str(name):newbal})
    elif int(x)==242:
      name="pushers"
      oldbal=ship["242"]
      formedbal.update({str(name):oldbal})
    elif int(x)==243:
      name="launchers"
      oldbal=ship["243"]
      formedbal.update({str(name):oldbal})
    elif int(x)==227:
      name="rcs"
      oldbal=ship["227"]
      formedbal.update({str(name):oldbal})
    elif int(x)==228:
      name="bursts"
      oldbal=ship["228"]
      formedbal.update({str(name):oldbal})
    elif int(x)==229:
      name="autos"
      oldbal=ship["229"]
      formedbal.update({str(name):oldbal})
    elif int(x)==252:
      name="loaders"
      oldbal=ship["252"]
      formedbal.update({str(name):oldbal})
    elif int(x)==234:
      name="ice"
      oldbal=ship["234"]
      formedbal.update({str(name):oldbal})
    elif int(x)==51 or int(x)==53 or int(x)==55 or int(x)==56:
      name="balls"
      old=formedbal[name]
      oldbal=ship[x]
      newbal=int(oldbal)+int(old)
      formedbal.update({str(name):newbal})
    elif int(x)==122:
      name="rcds"
      oldbal=ship["122"]
      formedbal.update({str(name):oldbal})
    else:
      asn=0
    #print(formedbal)
  #print(formedbal)
  return dict(formedbal)

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
    elif int(i)==227:
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
    #print(formedbal)
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
  data=readdata()
  data.pop(gid)
  setdata(data)
  gid=str(id)
  data=readdataB()
  data.pop(gid)
  setdataB(data)
  gid=str(id)
  data=readdataC()
  data.pop(gid)
  setdataC(data)
  gid=str(id)
  data=readdataD()
  data.pop(gid)
  setdataD(data)
  gid=str(id)
  data=readdataE()
  data.pop(gid)
  setdataE(data)
  data=readother()
  data["defaultdist"].pop(gid)
  setother(data)