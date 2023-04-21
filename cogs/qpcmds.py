import os, discord
import time
import pytz
import datetime 
#from keep_alive import keep_alive
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

class QPCmds(commands.Cog, name="QuickPing Commands",description="QuickPing System Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name='qp',help="Calls a ship from the QuickPing database. Format: n!qp shipname(as entered with no spaces in n!qpadd)")
  @commands.has_role('QuickPing')
  async def quickping(self, ctx, *, shipname):
    if str(ctx.message.author.id) not in banned:
      try:
        shipnameb=shipname.lower()
        gid = str(ctx.message.guild.id)
        lists.logback(ctx,shipname)
        await ctx.send(dumps(lists.readdataC()[gid][shipnameb]).replace('{','').replace('}', '').replace('"', ''))
      except KeyError:
        await ctx.send(f'KeyError: {shipname} Is not in the quickping database. Either {shipname} has not been entered into the list by a member or it is listed under a different key. Fixes: Capitalize the first letter (slugger -> Slugger), Use an abbreviation (Gamking Sniper 1 -> GKS1), or remove spaces in the name (Destruction Awaits You -> DestructionAwaitsYou). The solution could be a mix of the provided fixes.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
  
  
  @quickping.error
  async def quickping_error(self, ctx, error):
      if isinstance(error, commands.CheckFailure):
          await ctx.send('Error, Required Role: QuickPing, Not Found')
  
  @commands.command(name='qpadd',help="Adds a ship to the QuickPing database. Format is n!qp shiplink shipname(no spaces)")
  @commands.has_role('QuickPing')
  async def quickpingadd(self, ctx, *, msg):
    if str(ctx.message.author.id) not in banned:
      gid = str(ctx.message.guild.id)
      msgparts, data = msg.split(" "), lists.readdataC()
      ping = "@here"
      link=msgparts[1]
      linkb=link.lower()
      print(linkb)
      pinger = ping + linkb
      data[gid][linkb]=str(pinger)
      lists.setdataC(data)
      lists.logback(ctx,msg)
      await ctx.send(f'Added {msgparts[1]} with a link of {msgparts[0]} to the QuickPing database.')
    #await ctx.send(dumps(readdataC()[msg]).replace('{','').replace('}', '').replace('"', ''))
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
  
  
  @quickpingadd.error
  async def quickpingadd_error(self, ctx, error):
      if isinstance(error, commands.CheckFailure):
          await ctx.send('Error, Required Role: QuickPing, Not Found')

  @commands.command(name='qpdel')
  @commands.has_role('QuickPing')
  async def qpdelete(self,ctx,ship):
    if str(ctx.message.author.id) in banned:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
    elif str(ctx.message.author.id) not in banned:
      lists.logback(ctx,ship)
      gid = str(ctx.message.guild.id)
      name=str(ship).lower()
      data=lists.readdataC()
      del data[gid][name]
      try:
        lists.setdataC(data)
        await ctx.send(f'Removed {ship} from the QuickPing list in {ctx.message.guild.name}')
      except KeyError:
        await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
    else:
      await ctx.send("Error, I hit a wall checking your ID against my banned users list. Please try running the command again.")

  @qpdelete.error
  async def qpdelete_error(self, ctx, error):
      if isinstance(error, commands.CheckFailure):
          await ctx.send('Error, Required Role: QuickPing, Not Found')

async def setup(bot: commands.Bot):
    await bot.add_cog(QPCmds(bot))