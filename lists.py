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
    return loads(open('distribution.json', 'r').read())

def setdata(data):
    with open("distribution.json", "w") as f:
        f.write(dumps(data))

def readdataB():
    return loads(open("relations.json","r").read())

def setdataB(dataB):
    with open("relations.json", "w") as g:
        g.write(dumps(dataB))

def readdataC():
    return loads(open('quickping.json', 'r').read())

def setdataC(dataC):
    with open("quickping.json", "w") as g:
        g.write(dumps(dataC))

def readdataD():
    return loads(open('designs.json', 'r').read())

def setdataD(dataD):
    with open("designs.json", "w") as g:
        g.write(dumps(dataD))
      
def readdataE():
    return loads(open('config.json', 'r').read())

def setdataE(datae):
    with open("config.json", "w") as h:
        h.write(dumps(datae))

def readother():
    return loads(open('other.json', 'r').read())

def setother(datah):
    with open("other.json", "w") as f:
        f.write(dumps(datah))

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
    g.write(f'Command run at {ct}, by {usern} (User ID: {userid}), in server {guildn} (Server ID: {guildid}). Command Run: {commandrun}, Command Contents: {mesg}')
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
    
async def updatemsg(gid):
  #readother()
  role = "OfficialMember" #"OfficialMember"
  #guild = Member.guild
  loc = "MemChn"
  guild = ctx.get_guild(7547780206399325) 
  role_name = role
  await guild.fetch_roles()
  msg = await guild.fetch_message(int(1033752202356981801))
  #bot.get_guild(754778020639932516)
  key = "MemChn"
  print(guild)
  channel = guild.get_channel(754778311573635213)
  for member in guild.members:
    if role_name in member.roles:
      await ctx.send(f"{member.display_name} - {member.id}")
  #await msg.edit(content="")
  print(channel)

async def logmajor(bot,ctx,msg):
  #Major Event Logging (To Channel In Developmnt Server)(Events Logged Are: Authorizing Users, Bans, Joins)
  tz = pytz.timezone('America/New_York')
  ct = datetime.datetime.now(tz)
  myguild = bot.get_guild(1031900634741473280)
  channel = myguild.get_channel(1037788623015268444)
  await channel.send(f'<@{930284432634556496}> !MAJOR EVENT! Command Run: {ctx.invoked_With}. Command Run At {ct} by {ctx.message.author.name} (User Id: {ctx.message.author.id}) in server {ctx.message.guild.name} (Server ID:{ctx.message.guild.id}. The Command Contained The Following Data: {msg}.')
  
    
def checkperms(ctx):
  #bannedlist()
  gid = str(ctx.message.guild.id)
  uid = str(ctx.message.author.id)
  keya="auth"
  autho = dumps(readdataE()[gid][keya])
  if str(uid) not in banned:
    if str(uid) in autho:
      return True
    elif str(uid) not in autho:
      return False
    else:
      return False
  elif str(uid) in banned:
    return False
  else:
    return False