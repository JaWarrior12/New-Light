import os, discord
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

#Lists
import lists
#Auth For Leadership Commands
authorized = lists.authorized
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
lists.checkperms(ctx,msg)

class DistCmds(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name="logloot",brief="Adds/Subtracts loot from a user's balance.")
  async def returnpaymentdata(ctx, *, msg):
    if ctx.message.author.id not in banned:
      if ctx.message.author.id in authorized:
        msgparts, data = msg.split(" "), lists.readdata()
        lists.logback(ctx,msg)
        a = "NLC"
        b = "BOC"
        c = "TestServer"
        d= "DSR"
        e= "FRF"
        nf = int(dumps(lists.readdata()[msgparts[0]][msgparts[1]][msgparts[2]]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        ns = int(msgparts[3])
        added = ns + nf
        if lists.getguild(ctx) == NLC:
          if ctx.message.author.id in nlcauth:
            if msgparts[0] == a:
              data[msgparts[0]][msgparts[1]][msgparts[2]] = int(added)
              lists.setdata(data)
              await ctx.send(f'now {msgparts[1]} has {added} {msgparts[2]} in {msgparts[0]}')
            else:
             await ctx.send('Error! Please use n!logloot NLC "username" "item" "new value"! You can only run NLC update commands in the NLC server')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == BOC:
          if ctx.message.author.id in bocauth:
            if msgparts[0] == b:
              print(1)
              data[msgparts[0]][msgparts[1]][msgparts[2]] = int(added)
              lists.setdata(data)
              await ctx.send(f'now {msgparts[1]} has {added} {msgparts[2]} in {msgparts[0]}')
            else:
              await ctx.send('Error! Please use n!logloot BOC "username" "item" "new value"! You can only run BOC update commands in the BOC server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')  
        elif lists.getguild(ctx) == TestSrvr:
          if ctx.message.author.id in tsauth:
            print(2)
            if msgparts[0] == c:
              data[msgparts[0]][msgparts[1]][msgparts[2]] = int(added)
              lists.setdata(data)
              await ctx.send(f'now {msgparts[1]} has {added} {msgparts[2]} in {msgparts[0]}')
            else:
              await ctx.send('Error! Please use n!logloot TestServer "username" "item" "new value"! You can only run TestServer update commands in the TestServer server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == DSR:
          if ctx.message.author.id in dsrauth:
            print(2)
            if msgparts[0] == d:
              data[msgparts[0]][msgparts[1]][msgparts[2]] = int(msgparts[3])
              lists.setdata(data)
              await ctx.send(f'now {msgparts[1]} has {msgparts[added]} {msgparts[2]} in {msgparts[0]}')
            else:
              await ctx.send('Error! Please use n!logloot DSR "username" "item" "new value"! You can only run DSR update commands in the DSR server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == FRF:
          if ctx.message.author.id in ffauth:
            print(2)
            if msgparts[0] == e:
              data[msgparts[0]][msgparts[1]][msgparts[2]] = int(added)
              lists.setdata(data)
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


  @commands.command(name='reset',brief="Resets one loot value in a user's balance.")
  async def resetalldata(self,ctx, *, msg):
    if ctx.message.author.id not in banned:
      if ctx.message.author.id in authorized:
        msgparts, data = msg.split(" "), lists.readdata()
        a = "NLC"
        b = "BOC"
        c = "TestServer"
        d = "DSR"
        e = "FRF"
        lists.logback(ctx,msg)
        mesg = data[msgparts[0]][msgparts[1]][msgparts[2]]=d
        if lists.getguild(ctx) == NLC:
          if ctx.message.author.id in nlcauth:
            if msgparts[0] == a:
              print(1)
              #data = readdata()
              #for i in data[mesg].keys():
              #data[mesg][i] = 0
              lists.setdata(data)
              await ctx.send('User Data Reset')
            else:
              await ctx.send('Error! Please use n!reset NLC "username" "item"! You can only run NLC update commands in the NLC server')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == BOC:
          if ctx.message.author.id in bocauth:
            if msgparts[0] == b:
              print(2)
              #data = readdata()
              #for i in data[mesg].keys():
              #data[mesg][i] = 0
              lists.setdata(data)
              await ctx.send('User Data Reset')
            else:
              await ctx.send('Error! Please use n!reset BOC "username" "item"! You can only run BOC update commands in the BOC server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == TestSrvr:
          if ctx.message.author.id in tsauth:
            if msgparts[0] == c:
              print(3)
              #data = readdata()
              #for i in data[mesg].keys():
                #data[mesg][i] = 0
              lists.setdata(data)
              await ctx.send('User Data Reset')
            else:
              await ctx.send('Error! Please use n!reset TestServer "username" "item"! You can only run TestServer update commands in the TestServer server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == DSR:
          if ctx.message.author.id in dsrauth:
            if msgparts[0] == d:
              print(3)
              #data = readdata()
              #for i in data[mesg].keys():
              #data[mesg][i] = 0
              list.setdata(data)
              await ctx.send('User Data Reset')
            else:
              await ctx.send('Error! Please use n!reset DSR "username" "item"! You can only run DSR update commands in the DSR server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == FRF:
          if ctx.message.author.id in ffauth:
            if msgparts[0] == e:
              print(3)
              #data = readdata()
              #for i in data[mesg].keys():
              #data[mesg][i] = 0
              list.setdata(data)
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

  @commands.command(name='balance',brief="Calls a user's balance.")
  async def getuserloot(self,ctx, *, msg):
    if ctx.message.author.id not in banned:
        msgparts, data = msg.split(" "), lists.readdata()
        a = "NLC"
        b = "BOC"
        c = "TestServer"
        d = "DSR"
        e = "FRF"
        p1 = msgparts[0]
        p2 = msgparts[1]
        p3 = p1
        lists.logback(ctx,msg)
        #data[msgparts[0]]=str(msgparts[1])
        #print(data)
        if lists.getguild(ctx) == NLC:
          if msgparts[0] == a:
            print(1)
            await ctx.send(dumps(lists.readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
          else:
           await ctx.send('Error! Please use n!balance NLC "username"! You can only run NLC commands in the NLC server')
        elif lists.getguild(ctx) == BOC:
          if msgparts[0] == b:
            print(2)
            await ctx.send(dumps(lists.readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
          else:
           await ctx.send('Error! Please use n!balance BOC "username"! You can only run BOC commands in the BOC server!')
        elif lists.getguild(ctx) == TestSrvr:
          print(3)
          if msgparts[0] == c:
              await ctx.send(dumps(list.readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!balance TestServer "username"! You can only run TestServer commands in the TestServer server!')
        elif lists.getguild(ctx) == DSR:
          print(3)
          if msgparts[0] == d:
              await ctx.send(dumps(lists.readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!balance DSR "username"! You can only run DSR commands in the DSR server!')
        elif lists.getguild(ctx) == FRF:
          print(3)
          if msgparts[0] == e:
              await ctx.send(dumps(list.readdata()[p1][p2]).replace(':','=').replace('{','').replace('}','').replace('"',''))
          else:
            await ctx.send('Error! Please use n!balance FRF "username"! You can only run FRF commands in the FRF server!')
        else:
            await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

  @commands.command(name="addmember",brief="Adds a member to the clan's distribution database.")
  async def addmember(self,ctx, *, msg):
    if ctx.message.author.id not in banned:
      if ctx.message.author.id in authorized:
        msgparts, data = msg.split(" "), lists.readdata()
        a = "NLC"
        b = "BOC"
        c = "TestServer"
        d = "DSR"
        e = "FRF"
        lists.logback(ctx,msg)
        inputv = {"flux":0,"loaders":0,"rcs":0,"pushers":0}
        if lists.getguild(ctx) == NLC:
          if ctx.message.author.id in nlcauth:
            if msgparts[0] == a:
              data[msgparts[0]][msgparts[1]]=dict(inputv)
              lists.setdata(data)
              await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
            else:
             await ctx.send('Error! Please use n!addmember NLC "username (NO SPACES)"! You can only run NLC update commands in the NLC server')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == BOC:
          if ctx.message.author.id in bocauth:
            if msgparts[0] == b:
              print(1)
              data[msgparts[0]][msgparts[1]]=dict(inputv)
              lists.setdata(data)
              await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
            else:
             await ctx.send('Error! Please use n!addmember BOC "username (NO SPACES)"! You can only run BOC update commands in the BOC server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == TestSrvr:
          if ctx.message.author.id in tsauth:
            print(2)
            if msgparts[0] == c:
              data[msgparts[0]][msgparts[1]]=dict(inputv)
              lists.setdata(data)
              await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
            else:
              await ctx.send('Error! Please use n!addmember TestServer "username (NO SPACES)"! You can only run TestServer update commands in the TestServer server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == DSR:
          if ctx.message.author.id in tsauth:
            print(2)
            if msgparts[0] == d:
              data[msgparts[0]][msgparts[1]]=dict(inputv)
              lists.setdata(data)
              await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
            else:
              await ctx.send('Error! Please use n!addmember DSR "username (NO SPACES)"! You can only run DSR update commands in the DSR server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == FRF:
          if ctx.message.author.id in ffauth:
            print(2)
            if msgparts[0] == e:
              data[msgparts[0]][msgparts[1]]=dict(inputv)
              lists.setdata(data)
              await ctx.send(f'Added {msgparts[1]} to the distribution list in {msgparts[0]}')
            else:
              await ctx.send('Error! Please use n!addmember FRF "username (NO SPACES)"! You can only run FRF update commands in the FRF server!')
        else:
            await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
      else:
          await ctx.send('Unapproved Operator.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

  @commands.command(name="removemember",brief="Removes a member from a clan's distribution database.")
  async def remmem(self,ctx, *, msg):
    if ctx.message.author.id not in banned:
      if ctx.message.author.id in authorized:
        msgparts, data = msg.split(" "), lists.readdata()
        a = "NLC"
        b = "BOC"
        c = "TestServer"
        d = "DSR"
        e = "FRF"
        data = lists.readdata()
        del data[msgparts[0]][msgparts[1]]
        lists.logback(ctx,msg)
        if lists.getguild(ctx) == NLC:
          if ctx.message.author.id in nlcauth:
            if msgparts[0] == a:
              lists.setdata(data)
              await ctx.send(f'Removed {msgparts[1]} from the distribution list in {msgparts[0]}')
            else:
             await ctx.send('Error! Please use n!removemember NLC "username (NO SPACES)"! You can only run NLC update commands in the NLC server')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == BOC:
          if ctx.message.author.id in bocauth:
            if msgparts[0] == b:
              print(1)
              lists.setdata(data)
              await ctx.send(f'Removed {msgparts[1]} from the distribution list in {msgparts[0]}')
            else:
             await ctx.send('Error! Please use n!removemember BOC "username (NO SPACES)"! You can only run BOC update commands in the BOC server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == TestSrvr:
          if ctx.message.author.id in tsauth:
            print(2)
            if msgparts[0] == c:
              lists.setdata(data)
              await ctx.send(f'Removed {msgparts[1]} from the distribution list in {msgparts[0]}')
            else:
              await ctx.send('Error! Please use n!removemember TestServer "username (NO SPACES)"! You can only run TestServer update commands in the TestServer server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == DSR:
          if ctx.message.author.id in dsrauth:
            print(2)
            if msgparts[0] == d:
              data[msgparts[0]][msgparts[1]]=dict(inputv)
              lists.setdata(data)
              await ctx.send(f'Removed {msgparts[1]} to the distribution list in {msgparts[0]}')
            else:
              await ctx.send('Error! Please use n!removemember DSR "username (NO SPACES)"! You can only run DSR update commands in the DSR server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == FRF:
          if ctx.message.author.id in ffauth:
            print(2)
            if msgparts[0] == e:
              data[msgparts[0]][msgparts[1]]=dict(inputv)
              lists.setdata(data)
              await ctx.send(f'Removed {msgparts[1]} to the distribution list in {msgparts[0]}')
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

  @commands.command(name='balall',brief="Calls all balances in a clan's distribution database. ")
  async def balanceall(self,ctx,*,msg):
    if ctx.message.author.id not in banned:
      if ctx.message.author.id in authorized:
        msgparts, data = msg.split(" "), lists.readdata()
        a = "NLC"
        b = "BOC"
        c = "TestServer"
        d = "DSR"
        e = "FRF"
        lists.logback(ctx,msg)
        mesg = str(msgparts[0])
        if lists.getguild(ctx) == NLC:
          if ctx.message.author.id in nlcauth:
            if msgparts[0] == a:
              print(1)
              await ctx.send('Balances Of All Members')
              await ctx.send(dumps(lists.readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
            else:
              await ctx.send('Error! Please use n!balall NLC! You can only run NLC update commands in the NLC server')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')    
        elif lists.getguild(ctx) == BOC:
          if ctx.message.author.id in bocauth:
            if msgparts[0] == b:
              print(2)
              await ctx.send('Balances Of All Members')
              await ctx.send(dumps(lists.readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
            else:
             await ctx.send('Error! Please use n!balall BOC! You can only run BOC update commands in the BOC server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')  
        elif lists.getguild(ctx) == TestSrvr:
          if ctx.message.author.id in tsauth:
            if msgparts[0] == c:
              print(3)
              await ctx.send('Balances Of All Members')
              await ctx.send(dumps(lists.readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
            else:
              await ctx.send('Error! Please use n!balall TestServer! You can only run TestServer update commands in the TestServer server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == DSR:
          if ctx.message.author.id in dsrauth:
            if msgparts[0] == d:
              print(3)
              await ctx.send('Balances Of All Members')
              await ctx.send(dumps(lists.readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
            else:
              await ctx.send('Error! Please use n!balall DSR! You can only run DSR update commands in the DSR server!')
          else:
            await ctx.send('You are NOT Authorized to use leadership commands in this server.')
        elif lists.getguild(ctx) == FRF:
          if ctx.message.author.id in ffauth:
            if msgparts[0] == e:
              print(3)
              await ctx.send('Balances Of All Members')
              await ctx.send(dumps(lists.readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
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

def setup(bot: commands.Bot):
    bot.add_cog(DistCmds(bot))
