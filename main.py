import os, discord
<<<<<<< HEAD
from os import system
=======
>>>>>>> origin/main
import time
import pytz
import datetime 
from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup

#Import Lists
import lists
<<<<<<< HEAD

lists.bannedlist()

intents = discord.Intents.default()
intents.members = True

client = discord.Client()

bot = commands.Bot(command_prefix='n!',intents=intents)

#SAVE THIS CODE \/!!!
#class MyHelp(commands.HelpCommand): 
    #async def send_bot_help(self, mapping):
      #channel = self.get_destination()
      #with open('Documentation.txt', 'rb') as fp:
         #await channel.send(file=discord.File(fp, 'New Light Documentation'))
=======

intents = discord.Intents.default()
intents.members = True

client = discord.Client()

#Auth For Leadership Commands
authorized = lists.authorized #[949451462151376948, 722703947638505556, 445763770799620097, 907899780561272842, 872718294023569408,930806975950909451]
banned = lists.banned #[948934984088035408,975761604975153233]
developers = lists.developers #[949451462151376948,722703947638505556]

bot = commands.Bot(command_prefix='n!',intents=intents)

#Authorized Based On Clan
nlcauth = lists.nlcauth #[949451462151376948,445763770799620097]
bocauth = lists.bocauth #[949451462151376948,907899780561272842]
dsrauth = lists.dsrauth #[949451462151376948,872718294023569408]
tsauth = lists.tsauth #[949451462151376948,722703947638505556]
ffauth = lists.ffauth #[949451462151376948,930806975950909451]

#Server IDs
NLC = lists.NLC #754778020639932516
BOC = lists.BOC #966067610779271168
TestSrvr = lists.TestSrvr #975858783504969808
DSR = lists.DSR #872725039097720883
FRF = lists.FRF #952133314137956362

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
      channel = self.get_destination()
      with open('Documentation.txt', 'rb') as fp:
        await channel.send(file=discord.File(fp, 'New Light Documentation'))
>>>>>>> origin/main
        #f = open("Documentation.txt", "r")
        #if f.mode == 'r':
        #    contents = f.read()
        #    await channel.send("New Light Documentation")
        #    await channel.send(contents)

class MyHelp(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()

<<<<<<< HEAD
#bot.help_command = commands.DefaultHelpCommand() #MyHelp()

version = "3.2.0"
=======
version = "1.9.5"
>>>>>>> origin/main

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    activity = discord.Game(name=f"JaWarrior.py & n!help. Version: {version}", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    #channel = client.get_channel(974078794065403924)
    #await channel.send("I'm Logged In")

<<<<<<< HEAD
@bot.event
async def on_guild_join(guild):
    #guild=before
    myguild = bot.get_guild(1031900634741473280)
    channel = myguild.get_channel(1037788623015268444)
    invite = await guild.system_channel.create_invite(reason="Inviting My Developer To Your Amazing Server!")

    e = discord.Embed(title="I've joined a server.")
    e.add_field(name="Server Name", value=guild.name, inline=False)
    e.add_field(name="Invite Link", value=invite, inline=False)
    e.set_thumbnail(url=guild.icon_url)
    await channel.send(embed=e)
    await channel.send(f'Guild Name: {guild}')
    await channel.send(f'Guild Id: {guild.id}')

@bot.event
async def on_disconnect():
  tz = pytz.timezone('America/New_York')
  ct = datetime.datetime.now(tz)
  print("Disconnected")
  #print(data)
  with open("Backups/disconnectlogs.txt", "a+") as o:
    o.write('\n')
    o.write(f'New Light disconnected from the DISCORD platform at {ct}.')
    o.write('\n')
  
#Load Cogs (My Way)
bot.load_extension("cogs.errorhand")
bot.load_extension("cogs.relcmds")
bot.load_extension("cogs.distcmds")
bot.load_extension("cogs.descmds")
bot.load_extension("cogs.qpcmds")
bot.load_extension("cogs.othercmds")
bot.load_extension("cogs.econcmds")
bot.load_extension("cogs.devcmds")

#Load Cogs Other Way
#extensions = ['DevCmds']

#if __name__ == '__main__':  # Ensures this is the file being ran
	#for extension in extensions:
		#bot.load_extension(extension)  # Loades every extension.
=======
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

@bot.command(name="logloot")
async def returnpaymentdata(ctx, *, msg):
  if ctx.message.author.id not in banned:
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdata()
      logback(ctx,msg)
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d= "DSR"
      e= "FRF"
      nf = int(dumps(readdata()[msgparts[0]][msgparts[1]][msgparts[2]]).replace(':','=').replace('{','').replace('}','').replace('"',''))
      ns = int(msgparts[3])
      added = ns + nf
      if getguild(ctx) == NLC:
        if ctx.message.author.id in nlcauth:
          if msgparts[0] == a:
            data[msgparts[0]][msgparts[1]][msgparts[2]] = int(added)
            setdata(data)
            await ctx.send(f'now {msgparts[1]} has {added} {msgparts[2]} in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!logloot NLC "username" "item" "new value"! You can only run NLC update commands in the NLC server')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == BOC:
        if ctx.message.author.id in bocauth:
          if msgparts[0] == b:
            print(1)
            data[msgparts[0]][msgparts[1]][msgparts[2]] = int(added)
            setdata(data)
            await ctx.send(f'now {msgparts[1]} has {added} {msgparts[2]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!logloot BOC "username" "item" "new value"! You can only run BOC update commands in the BOC server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')  
      elif getguild(ctx) == TestSrvr:
        if ctx.message.author.id in tsauth:
          print(2)
          if msgparts[0] == c:
            data[msgparts[0]][msgparts[1]][msgparts[2]] = int(added)
            setdata(data)
            await ctx.send(f'now {msgparts[1]} has {added} {msgparts[2]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!logloot TestServer "username" "item" "new value"! You can only run TestServer update commands in the TestServer server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in dsrauth:
          print(2)
          if msgparts[0] == d:
            data[msgparts[0]][msgparts[1]][msgparts[2]] = int(msgparts[3])
            setdata(data)
            await ctx.send(f'now {msgparts[1]} has {msgparts[added]} {msgparts[2]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!logloot DSR "username" "item" "new value"! You can only run DSR update commands in the DSR server!')
        else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == FRF:
        if ctx.message.author.id in ffauth:
          print(2)
          if msgparts[0] == e:
            data[msgparts[0]][msgparts[1]][msgparts[2]] = int(added)
            setdata(data)
            await ctx.send(f'now {msgparts[1]} has {added} {msgparts[2]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!logloot FRF "username" "item" "new value"! You can only run FRF update commands in the FRF server!')
        else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
        await ctx.send('Unapproved Operator.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')


@bot.command(name='reset')
async def resetalldata(ctx, *, msg):
  if ctx.message.author.id not in banned:
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      logback(ctx,msg)
      mesg = data[msgparts[0]][msgparts[1]][msgparts[2]]=d
      if getguild(ctx) == NLC:
        if ctx.message.author.id in nlcauth:
          if msgparts[0] == a:
            print(1)
            #data = readdata()
            #for i in data[mesg].keys():
            #data[mesg][i] = 0
            setdata(data)
            await ctx.send('User Data Reset')
          else:
            await ctx.send('Error! Please use n!reset NLC "username" "item"! You can only run NLC update commands in the NLC server')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == BOC:
        if ctx.message.author.id in bocauth:
          if msgparts[0] == b:
            print(2)
            #data = readdata()
            #for i in data[mesg].keys():
            #data[mesg][i] = 0
            setdata(data)
            await ctx.send('User Data Reset')
          else:
            await ctx.send('Error! Please use n!reset BOC "username" "item"! You can only run BOC update commands in the BOC server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == TestSrvr:
        if ctx.message.author.id in tsauth:
          if msgparts[0] == c:
            print(3)
            #data = readdata()
            #for i in data[mesg].keys():
              #data[mesg][i] = 0
            setdata(data)
            await ctx.send('User Data Reset')
          else:
            await ctx.send('Error! Please use n!reset TestServer "username" "item"! You can only run TestServer update commands in the TestServer server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in dsrauth:
          if msgparts[0] == d:
            print(3)
            #data = readdata()
            #for i in data[mesg].keys():
            #data[mesg][i] = 0
            setdata(data)
            await ctx.send('User Data Reset')
          else:
            await ctx.send('Error! Please use n!reset DSR "username" "item"! You can only run DSR update commands in the DSR server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == FRF:
        if ctx.message.author.id in ffauth:
          if msgparts[0] == e:
            print(3)
            #data = readdata()
            #for i in data[mesg].keys():
            #data[mesg][i] = 0
            setdata(data)
            await ctx.send('User Data Reset')
          else:
            await ctx.send('Error! Please use n!reset FRF "username" "item"! You can only run FRF update commands in the FRF server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
      await ctx.send('Unapproved Operator.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='balance')
async def getuserloot(ctx, *, msg):
  if ctx.message.author.id not in banned:
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      p1 = msgparts[0]
      p2 = msgparts[1]
      p3 = p1
      logback(ctx,msg)
      #data[msgparts[0]]=str(msgparts[1])
      #print(data)
      if getguild(ctx) == NLC:
        if msgparts[0] == a:
          print(1)
          await ctx.send(dumps(readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        else:
         await ctx.send('Error! Please use n!balance NLC "username"! You can only run NLC commands in the NLC server')
      elif getguild(ctx) == BOC:
        if msgparts[0] == b:
          print(2)
          await ctx.send(dumps(readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        else:
         await ctx.send('Error! Please use n!balance BOC "username"! You can only run BOC commands in the BOC server!')
      elif getguild(ctx) == TestSrvr:
        print(3)
        if msgparts[0] == c:
            await ctx.send(dumps(readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        else:
          await ctx.send('Error! Please use n!balance TestServer "username"! You can only run TestServer commands in the TestServer server!')
      elif getguild(ctx) == DSR:
        print(3)
        if msgparts[0] == d:
            await ctx.send(dumps(readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        else:
          await ctx.send('Error! Please use n!balance DSR "username"! You can only run DSR commands in the DSR server!')
      elif getguild(ctx) == FRF:
        print(3)
        if msgparts[0] == e:
            await ctx.send(dumps(readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        else:
          await ctx.send('Error! Please use n!balance FRF "username"! You can only run FRF commands in the FRF server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name="addmember")
async def addmember(ctx, *, msg):
  if ctx.message.author.id not in banned:
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      logback(ctx,msg)
      inputv = {"flux":0,"loaders":0,"rcs":0,"pushers":0}
      if getguild(ctx) == NLC:
        if ctx.message.author.id in nlcauth:
          if msgparts[0] == a:
            data[msgparts[0]][msgparts[1]]=dict(inputv)
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!addmember NLC "username (NO SPACES)"! You can only run NLC update commands in the NLC server')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == BOC:
        if ctx.message.author.id in bocauth:
          if msgparts[0] == b:
            print(1)
            data[msgparts[0]][msgparts[1]]=dict(inputv)
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!addmember BOC "username (NO SPACES)"! You can only run BOC update commands in the BOC server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == TestSrvr:
        if ctx.message.author.id in tsauth:
          print(2)
          if msgparts[0] == c:
            data[msgparts[0]][msgparts[1]]=dict(inputv)
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!addmember TestServer "username (NO SPACES)"! You can only run TestServer update commands in the TestServer server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in tsauth:
          print(2)
          if msgparts[0] == d:
            data[msgparts[0]][msgparts[1]]=dict(inputv)
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!addmember DSR "username (NO SPACES)"! You can only run DSR update commands in the DSR server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == FRF:
        if ctx.message.author.id in ffauth:
          print(2)
          if msgparts[0] == e:
            data[msgparts[0]][msgparts[1]]=dict(inputv)
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!addmember FRF "username (NO SPACES)"! You can only run FRF update commands in the FRF server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
        await ctx.send('Unapproved Operator.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name="removemember")
async def remmem(ctx, *, msg):
  if ctx.message.author.id not in banned:
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      data = readdata()
      del data[msgparts[0]][msgparts[1]]
      logback(ctx,msg)
      if getguild(ctx) == NLC:
        if ctx.message.author.id in nlcauth:
          if msgparts[0] == a:
            setdata(data)
            await ctx.send(f'Removed {msgparts[1]} from the distribution list in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!removemember NLC "username (NO SPACES)"! You can only run NLC update commands in the NLC server')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == BOC:
        if ctx.message.author.id in bocauth:
          if msgparts[0] == b:
            print(1)
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} from the distribution list in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!removemember BOC "username (NO SPACES)"! You can only run BOC update commands in the BOC server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == TestSrvr:
        if ctx.message.author.id in tsauth:
          print(2)
          if msgparts[0] == c:
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} from the distribution list in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!removemember TestServer "username (NO SPACES)"! You can only run TestServer update commands in the TestServer server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in dsrauth:
          print(2)
          if msgparts[0] == d:
            data[msgparts[0]][msgparts[1]]=dict(inputv)
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!removemember DSR "username (NO SPACES)"! You can only run DSR update commands in the DSR server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == FRF:
        if ctx.message.author.id in ffauth:
          print(2)
          if msgparts[0] == e:
            data[msgparts[0]][msgparts[1]]=dict(inputv)
            setdata(data)
            await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!removemember FRF "username (NO SPACES)"! You can only run FRF update commands in the FRF server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
        await ctx.send('Unapproved Operator.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='rel')
async def relations(ctx, *, msg):
  if ctx.message.author.id not in banned:
      msgparts, data = msg.split(" "), readdataB()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      p1 = msgparts[0]
      p2 = msgparts[1]
      logback(ctx,msg)
      #mesg = data[msgparts[0]][msgparts[1]]=str(msgparts[2])
      if getguild(ctx) == NLC:
        if msgparts[0] == a:
          print(1)
          await ctx.send(dumps(readdataB()[p1][p2]).replace(':', '=').replace('{', '').replace('}', '').replace('"', ''))
        else:
          await ctx.send('Error! Please use n!rel NLC "clan"! You can only run NLC commands in the NLC server')
      elif getguild(ctx) == BOC:
        if msgparts[0] == b:
          print(2)
          await ctx.send(dumps(readdataB()[p1][p2]).replace(':', '=').replace('{', '').replace(
            '}', '').replace('"', ''))
        else:
         await ctx.send('Error! Please use n!rel BOC "clan"! You can only run BOC commands in the BOC server!')
      elif getguild(ctx) == TestSrvr:
        if msgparts[0] == c:
          print(3)
          await ctx.send(dumps(readdataB()[p1][p2]).replace(':', '=').replace('{', '').replace(
            '}', '').replace('"', ''))
        else:
          await ctx.send('Error! Please use n!rel TestServer "clan"! You can only run TestServer commands in the TestServer server!')
      elif getguild(ctx) == DSR:
        if msgparts[0] == d:
          print(3)
          await ctx.send(dumps(readdataB()[p1][p2]).replace(':', '=').replace('{', '').replace(
            '}', '').replace('"', ''))
        else:
          await ctx.send('Error! Please use n!rel DSR "clan"! You can only run DSR commands in the DSR server!')
      elif getguild(ctx) == FRF:
        if msgparts[0] == e:
          print(3)
          await ctx.send(dumps(readdataB()[p1][p2]).replace(':', '=').replace('{', '').replace(
            '}', '').replace('"', ''))
        else:
          await ctx.send('Error! Please use n!rel FRF "clan"! You can only run FRF commands in the FRF server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='qp')
@commands.has_role('QuickPing')
async def quickping(ctx, *, msg):
  if ctx.message.author.id not in banned:
    logback(ctx,msg)
    await ctx.send(dumps(readdataC()[msg]).replace('{','').replace('}', '').replace('"', ''))
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')


@quickping.error
async def quickping_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Error, Required Role: QuickPing, Not Found')

@bot.command(name='qpadd')
@commands.has_role('QuickPing')
async def quickpingadd(ctx, *, msg):
  if ctx.message.author.id not in banned:
    msgparts, data = msg.split(" "), readdataC()
    ping = "@here "
    pinger = ping + msgparts[0]
    data[msgparts[1]]=str(pinger)
    setdataC(data)
    logback(ctx,msg)
    await ctx.send(f'Added {msgparts[1]} with a link of {msgparts[0]} to the QuickPing database.')
  #await ctx.send(dumps(readdataC()[msg]).replace('{','').replace('}', '').replace('"', ''))
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')


@quickpingadd.error
async def quickpingadd_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Error, Required Role: QuickPing, Not Found')

@bot.command(name='balall')
async def balanceall(ctx,*,msg):
  if ctx.message.author.id not in banned:
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      logback(ctx,msg)
      mesg = str(msgparts[0])
      if getguild(ctx) == NLC:
        if ctx.message.author.id in nlcauth:
          if msgparts[0] == a:
            print(1)
            await ctx.send('Balances Of All Members')
            await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!balall NLC! You can only run NLC update commands in the NLC server')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')    
      elif getguild(ctx) == BOC:
        if ctx.message.author.id in bocauth:
          if msgparts[0] == b:
            print(2)
            await ctx.send('Balances Of All Members')
            await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
          else:
           await ctx.send('Error! Please use n!balall BOC! You can only run BOC update commands in the BOC server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')  
      elif getguild(ctx) == TestSrvr:
        if ctx.message.author.id in tsauth:
          if msgparts[0] == c:
            print(3)
            await ctx.send('Balances Of All Members')
            await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!balall TestServer! You can only run TestServer update commands in the TestServer server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in dsrauth:
          if msgparts[0] == d:
            print(3)
            await ctx.send('Balances Of All Members')
            await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!balall DSR! You can only run DSR update commands in the DSR server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == FRF:
        if ctx.message.author.id in ffauth:
          if msgparts[0] == e:
            print(3)
            await ctx.send('Balances Of All Members')
            await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!balall FRF! You can only run FRF update commands in the FRF server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    #await ctx.send(  dumps(readdata()).replace(':','=').replace('{','').replace('}','').replace('"',''))
    #await ctx.send('Balances Of All Members')
    #await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
    else:
      await ctx.send('Unapproved Operator.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name="changerel")
async def changerel(ctx, *, msg):
  if ctx.message.author.id not in banned:
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdataB()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      logback(ctx,msg)
      if getguild(ctx) == NLC:
        if ctx.message.author.id in nlcauth:
          if msgparts[0] == a:
            data[msgparts[0]][msgparts[1]]=str(msgparts[2])
            setdataB(data)
            await ctx.send(f'now {msgparts[1]} has a relation of {msgparts[2]} in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!changerel NLC "clan" "new relation! You can only run NLC update commands in the NLC server')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == BOC:
        if ctx.message.author.id in bocauth:
          if msgparts[0] == b:
            print(1)
            data[msgparts[0]][msgparts[1]]=str(msgparts[2])
            setdataB(data)
            await ctx.send(f'now {msgparts[1]} has a relation of {msgparts[2]} in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!changerel BOC "clan" "new relation"! You can only run BOC update commands in the BOC server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == TestSrvr:
        if ctx.message.author.id in tsauth:
          print(2)
          if msgparts[0] == c:
            data[msgparts[0]][msgparts[1]]=str(msgparts[2])
            setdataB(data)
            await ctx.send(f'now {msgparts[1]} has a relation of {msgparts[2]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!changerel TestServer "clan" "new relation"! You can only run TestServer update commands in the TestServer server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in dsrauth:
          print(2)
          if msgparts[0] == d:
            data[msgparts[0]][msgparts[1]]=str(msgparts[2])
            setdataB(data)
            await ctx.send(f'now {msgparts[1]} has a relation of {msgparts[2]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!changerel DSR "clan" "new relation"! You can only run DSR update commands in the DSR server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in ffauth:
          print(2)
          if msgparts[0] == e:
            data[msgparts[0]][msgparts[1]]=str(msgparts[2])
            setdataB(data)
            await ctx.send(f'now {msgparts[1]} has a relation of {msgparts[2]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!changerel FRF "clan" "new relation"! You can only run FRF update commands in the FRF server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
        await ctx.send('Unapproved Operator.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name="addrel")
async def addrel(ctx, *, msg):
  if ctx.message.author.id not in banned:
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdataB()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      logback(ctx,msg)
      if getguild(ctx) == NLC:
        if ctx.message.author.id in nlcauth:
          if msgparts[0] == a:
            data[msgparts[0]][msgparts[2]]=str(msgparts[1])
            setdataB(data)
            await ctx.send(f'now {msgparts[2]} has a relation of {msgparts[1]} in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!addrel NLC "relation" "clan name (NO SPACES)"! You can only run NLC update commands in the NLC server')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == BOC:
        if ctx.message.author.id in bocauth:
          if msgparts[0] == b:
            print(1)
            data[msgparts[0]][msgparts[2]]=str(msgparts[1])
            setdataB(data)
            await ctx.send(f'now {msgparts[2]} has a relation of {msgparts[1]} in {msgparts[0]}')
          else:
           await ctx.send('Error! Please use n!addrel BOC "relation" "clan name (NO SPACES)"! You can only run BOC update commands in the BOC server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == TestSrvr:
        if ctx.message.author.id in tsauth:
          print(2)
          if msgparts[0] == c:
            data[msgparts[0]][msgparts[2]]=str(msgparts[1])
            setdataB(data)
            await ctx.send(f'now {msgparts[2]} has a relation of {msgparts[1]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!addrel TestServer "relation" "clan name (NO SPACES)"! You can only run TestServer update commands in the TestServer server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in dsrauth:
          print(2)
          if msgparts[0] == d:
            data[msgparts[0]][msgparts[2]]=str(msgparts[1])
            setdataB(data)
            await ctx.send(f'now {msgparts[2]} has a relation of {msgparts[1]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!addrel DSR "relation" "clan name (NO SPACES)"! You can only run DSR update commands in the DSR server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == FRF:
        if ctx.message.author.id in ffauth:
          print(2)
          if msgparts[0] == e:
            data[msgparts[0]][msgparts[2]]=str(msgparts[1])
            setdataB(data)
            await ctx.send(f'now {msgparts[2]} has a relation of {msgparts[1]} in {msgparts[0]}')
          else:
            await ctx.send('Error! Please use n!addrel FRF "relation" "clan name (NO SPACES)"! You can only run FRF update commands in the FRF server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
        await ctx.send('Unapproved Operator.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='relall')
async def relall(ctx,*,msg):
  if ctx.message.author.id not in banned:
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdataB()
      a = "NLC"
      b = "BOC"
      c = "TestServer"
      d = "DSR"
      e = "FRF"
      logback(ctx,msg)
      mesg = str(msgparts[0])
      if getguild(ctx) == NLC:
        if ctx.message.author.id in nlcauth:
          if msgparts[0] == a:
            print(1)
            await ctx.send('List of All Relations')
            await ctx.send(dumps(readdataB()[mesg]).replace(': "',' = ').replace('{','').replace(',','\n').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!relall NLC! You can only run NLC commands in the NLC server')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == BOC:
        if ctx.message.author.id in bocauth:
          if msgparts[0] == b:
            print(2)
            await ctx.send('List of All Relations')
            await ctx.send(dumps(readdataB()[mesg]).replace(': "',' = ').replace('{','').replace(',','\n').replace('}','').replace('"',''))
          else:
           await ctx.send('Error! Please use n!relall BOC! You can only run BOC commands in the BOC server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == TestSrvr:
        if ctx.message.author.id in tsauth:
          if msgparts[0] == c:
            print(3)
            await ctx.send('List of All Relations')
            await ctx.send(dumps(readdataB()[mesg]).replace(': "',' = ').replace('{','').replace(',','\n').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!relall TestServer! You can only run TestServer commands in the TestServer server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == DSR:
        if ctx.message.author.id in dsrauth:
          if msgparts[0] == d:
            print(3)
            await ctx.send('List of All Relations')
            await ctx.send(dumps(readdataB()[mesg]).replace(': "',' = ').replace('{','').replace(',','\n').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!relall DSR! You can only run DSR commands in the DSR server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      elif getguild(ctx) == FRF:
        if ctx.message.author.id in ffauth:
          if msgparts[0] == e:
            print(3)
            await ctx.send('List of All Relations')
            await ctx.send(dumps(readdataB()[mesg]).replace(': "',' = ').replace('{','').replace(',','\n').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!relall FRF! You can only run FRF commands in the FRF server!')
        else:
          await ctx.send('You are NOT Authorized to use leadership commands in this server.')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
        await ctx.send('Unapproved Operator.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='editdes')
async def fetchdesign(ctx, *, msg):
  if ctx.message.author.id not in banned:
    msgparts, data = msg.split(" "), readdataD()
    data[msgparts[0]][msgparts[1]] = str(msgparts[2])
    setdataD(data)
    logback(ctx,msg)
    await ctx.send(f'Now {msgparts[0]} has a {msgparts[1]} value of {msgparts[2]}.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='adddes')
async def savedesigns(ctx, *, msg):
  if ctx.message.author.id not in banned:
    msgparts, data = msg.split(" "), readdataD()
    auth = ctx.message.author.id
    auth2 = f'<@{auth}>'
    img = ctx.message.attachments[0]
    img2 = img.url
    #print(img2)
    default = {"Designer":auth2,"Image":img2}
    data[msgparts[0]]=dict(default)
    #print(data)
    setdataD(data)
    logback(ctx,msg)
    await ctx.send(f'Added {msgparts[0]} to the Database')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='deldes')
async def deldes(ctx, *, msg):
  if ctx.message.author.id not in banned:
    msgparts, data = msg.split(" "), readdataD()
    data = readdataD()
    del data[msgparts[0]]
    setdataD(data)
    logback(ctx,msg)
    await ctx.send(f'Deleted {msgparts[0]} from the Database')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='calldes')
async def calldes(ctx,*,msg):
  if ctx.message.author.id not in banned:
    msgparts, data = msg.split(" "), readdataD()
    data2 = msg.split(" ")
  #data[msgparts[0]][msgparts[1]] = str(msgparts[2])
  #data2[msgparts[0]][msgparts[1]]
  #p1 = msgparts[0]
    a = "all"
    b = "specific"
    logback(ctx,msg)
  #c = "categorysize"
    if msg == a:
      await ctx.send(dumps(readdataD()).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n'))
  #elif msgparts[0] == b:
   # await ctx.send(dumps(readdataD()[data]).replace(':', '=').replace('{', '').replace('}', '').replace('"', ''))
    elif msgparts[0] == b:
      await ctx.send(dumps(readdataD()[msgparts[1]]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n'))
  #elif msgparts[0] == c:
   # await ctx.send(dumps(readdataD())).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n')
    else:
      await ctx.send('Your input does not match any command, for n!calldes please use n!calldes category "category" or n!calldes all to call specific design groups.')
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name="memblist")
async def memblist(ctx,*,msg):
  if ctx.message.author.id in developers:
    ctx.send("This Command Is Not Ready Yet")
  else:
    ctx.send("You Are Not A Developer And Can Not Use This Command")

@bot.command(name='banuser')
async def banuser(ctx,*,msg):
  if ctx.message.author.id in developers:
    logback(ctx,msg)
    banned.append(msg)
    banner = ctx.message.author.name
    await ctx.send(f'{msg} has been banned from using New Light by {banner}')
    #await user.send(f'{msgparts[0]}: You have been BANNED from using New Light by {banner}. To appeal please DM JaWarrior#6752')
  else:
    ctx.send('YOU ARE NOT A DEVELOPER AND NOT ALLOWED TO BAN USERS FROM USING THE BOT!!!')

@bot.command(name='shutdown')
async def shutdown(ctx,msg=None):
  if ctx.message.author.id in developers:
    logback(ctx,msg)
    sdm = "NEW LIGHT Is Shutting Down Now And Will Be Back Online Shortly."
    channel = client.get_channel(974078794065403924)
    #await ctx.send("Published message: " + sdm)
    mesg = await ctx.send(sdm)
    await mesg.publish()
    backup(ctx)
    print('Backing Up Data')
    print('Shutting Down')
    await ctx.send('Shutting Down New Light')
    startup()
    await bot.logout()
  else:
    print(ctx.message.author.id)
    await ctx.send('ONLY DEVELOPERS ARE ALLOWED TO SHUTDOWN THE BOT!!! YOU ARE NOT A DEVELOPER') 

@bot.command(name='backup')
async def backups(ctx,*,msg=None):
  if ctx.message.author.id in developers:
    logback(ctx,msg)
    print('Backing Up')
    await ctx.send('Backing Up Data')
    backup(ctx)
  else:
    print(ctx.message.author.id)
    await ctx.send('ONLY DEVELOPERS ARE ALLOWED TO BACKUP THE BOT!!! YOU ARE NOT A DEVELOPER')

@bot.command(name='invite')
async def invite(ctx,*, msg=None):
  if ctx.message.author.id not in banned:
    user = await ctx.message.author.create_dm()
    await user.send(f'Hello there! I see you would like information on inviting me to your server. To start, please consider the following:')
    mesg = "1. JaWarrior#6752 has full control over me and can terminate your use at any time.;2. JaWarrior#6752 will require temporary administrator permissions to invite me to your server and set up 2 roles and a channel. The roles are QuickPing and OfficialMember, the channel is an announcement channel for updates to me.;3. All actions and commands are logged, abuse and spam will be delt with.;4. You are authorized to use leadership commands in your server only.;5. Special commands are only available to the developer, JaWarrior#6752. These commands are not discord related, they are for maintaining me.;6. Your User Id will be used for authorization;7. These are basic rules, and are subject to change.;8. Any questions can be directed to JaWarrior#6752"
    await user.send(mesg.replace(';','\n'))
    logback(ctx,msg)
    await user.send("If you wish to continue please DM JaWarrior#6752")
  else:
    await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

@bot.command(name='lockdown')
#@commands.has_permissions(manage_channels = True)
async def lockdown(ctx,*,msg=None):
  logback(ctx,msg)
  if ctx.message.author.id in developers:
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")
  else:
    await ctx.send(f'<@{ctx.message.author.id}> You Are NOT A Developer And CANNOT Lockdown Channels')

@bot.command(name='unlock')
#@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
  if ctx.message.author.id in developers:
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")
  else:
    await ctx.send(f'<@{ctx.message.author.id}> You Are NOT A Developer And CANNOT Unlock Channels')

def readother():
    return loads(open('other.json', 'r').read())


def setother(datah):
    with open("other.json", "w") as f:
        f.write(dumps(datah))

def updatemsg():
  readother()
  role = "BattlePing" #"OfficialMember"
  guild = Member.guild
  loc = "MemChn"
  print(guild)
  #guild = bot.get_guild(754778020639932516)
  #channel = guild.get_channel(754778311573635213)
  channel = guild.get_channel(dumps(readother()[loc][guild]))#.replace(':','=').replace('{','').replace('}','').replace('"',''))
  print(channel)
  channel.send("\n".join(str(member) for member in role.members))

@bot.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        newRole = next(role for role in after.roles if role not in before.roles)

        if newRole.name == "BattlePing": #OfficialMember
          print("MemList Updated")
          updatemsg()
        else:
          print("Not OfficialMember Role")

@bot.command(name='addrole',pass_context=True)
async def addrole(ctx, role: discord.Role, member: discord.Member=None):
  if ctx.message.author.id in developers:
    member = member or ctx.message.author
    print(member)
    print(role)
    await member.add_roles(role)
  else:
    ctx.send("Not A Dev")

@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Error: ')
    
#@bot.command(name='getid')
#@commands.has_role('Developer')
#turn this into callable function \/
#async def getguild(ctx):
  #id = ctx.message.guild.id
  #print(id)
#async def getguild(ctx):
 # id = ctx.message.guild.id
 # print(id)
>>>>>>> origin/main

#Load Cogs
bot.load_extension("cogs.errorhand")
bot.load_extension("cogs.devcmds")
#bot.load_extension("cogs.relcmds")
#bot.load_extension("cogs.distcmds")
#bot.load_extension("cogs.descmds")
#bot.load_extension("cogs.qpcmds")
      
#web socket for Uptimerobot to ping, keeps bot online
keep_alive()
bot.run(os.environ['token'])
