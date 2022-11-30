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

class RelCmds(commands.Cog, name="Relations Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name='rel',help="Calls a relation from a clan's relation database. Format: n!rel clan")
  async def relations(self,ctx, *, clan):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdataB()
        #chk = lists.checkperms(ctx,msg)
        gid = str(ctx.message.guild.id)
        p1 = gid
        p2 = clan
        lists.logback(ctx,clan)
        if str(ctx.message.author.id) not in banned:
          try:
            await ctx.send(dumps(lists.readdataB()[gid][clan]).replace(':', '=').replace('{', '').replace('}', '').replace('"', ''))
          except KeyError:
            await ctx.send(f'KeyError: {clan} Is not in the relations database. Either {clan} has not been entered into the list by a clan leader or it is listed under a different key. Fixes: Capitalize the first letter (cougar -> Cougar), Use an abbreviation (Swiss Armed Forces -> SAF), or remove spaces in the name (Hellenic League -> HellenicLeague). The solution could be a mix of the provided fixes.')
        else:
          await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
          return False
         
  @commands.command(name="changerel",help="Changes a clan's relation in their relations database. Format: n!changerel clan relation")
  async def changerel(self,ctx, clan, relation):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdataB()
        msgb = str(clan+" "+relation)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        lists.logback(ctx,msgb)
        if chk == True:
          try:
            data[gid][clan]=str(relation)
            lists.setdataB(data)
            await ctx.send(f'Now {clan} has a relation of {relation} in {ctx.message.guild.name}')
          except KeyError:
            await ctx.send(f'KeyError: {clan} Is not in the relations database. Either {clan} has not been entered into the list by a clan leader or it is listed under a different key. Fixes: Capitalize the first letter (cougar -> Cougar), Use an abbreviation (Swiss Armed Forces -> SAF), or remove spaces in the name (Hellenic League -> HellenicLeague). The solution could be a mix of the provided fixes.')
        else:
          return False
          
  
  @commands.command(name="addrel",help="Adds a relation to a clan's distribution database. Format: n!addrel clan relation")
  async def addrel(self,ctx,clan, relation):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdataB()
        msgb = str(clan+" "+relation)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        lists.logback(ctx,msgb)
        if chk == True:
          try:
            data[gid][clan]=str(relation)
            lists.setdataB(data)
            await ctx.send(f'Now {clan} has a relation of {relation} in {ctx.message.guild.name}')
            #def find_route(data, route_no):
              #return list(filter(lambda x: x.get(extra_key) == route_no, data))
            #route = find_route(jsondata,hexcode)
          except KeyError:
            await ctx.send(f'KeyError: {clan} Is not in the relations database. Either {clan} has not been entered into the list by a clan leader or it is listed under a different key. Fixes: Capitalize the first letter (cougar -> Cougar), Use an abbreviation (Swiss Armed Forces -> SAF), or remove spaces in the name (Hellenic League -> HellenicLeague). The solution could be a mix of the provided fixes.')
        else:
          return False
  
  @commands.command(name='relall',help="Calls all of a clan's relations in their relations database. Format: n!relall")
  async def relall(self,ctx,*,clan=None):
        #msgparts, data = msg.split(" "), lists.readdataB()
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        lists.logback(ctx,clan)
        mesg = str(gid)
        if chk == True:
              await ctx.send('List of All Relations')
              await ctx.send(dumps(lists.readdataB()[mesg]).replace(': "',' = ').replace('{','').replace(',','\n').replace('}','').replace('"',''))
        else:
          return False

  @commands.command(name="reltest",hidden=True)
  @commands.has_role("Developer")
  async def reltest(self,ctx,keya,keyb):
    await ctx.send("hi")
    datab=dumps(lists.readdataB())
    def find_route(data, route_no):
      return list(filter(lambda x: x.get(str(keyb)) == route_no, data))
    route = find_route(datab,keya)
    await ctx.send(route)

def setup(bot: commands.Bot):
    bot.add_cog(RelCmds(bot))