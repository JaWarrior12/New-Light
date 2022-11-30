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

class DistCmds(commands.Cog, name="Distribution Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name="logloot",brief="Adds/Subtracts loot from a user's balance.",help="Adds/Subtracts from a user's balance. The format is: n!logloot @User item amount. If you are subtracting make the amount negative.")
  async def returnpaymentdata(self, ctx, member: discord.Member, item, amount):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        msgb = str(member)+" "+item+" "+amount
        lists.logback(ctx,msgb)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        try:
          nf = int(dumps(lists.readdata()[gid][str(member)][str(item)]).replace(':','=').replace('{','').replace('}','').replace('"',''))
          ns = int(amount)
          added = ns + nf
          if chk == True:
                data[gid][str(member)][str(item)] = int(added)
                lists.setdata(data)
                await ctx.send(f'Now {member} has {added} {item} in {ctx.message.guild.name}')
        except KeyError:
          await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
          
  @commands.command(name='reset',help="Resets one loot value in a user's balance. Format: n!reset @User item")
  async def resetalldata(self, ctx, member: discord.Member, item):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        msgb=str(member)+" "+item
        lists.logback(ctx,msgb)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        if chk == True:
          try:
            data[gid][str(member)][str(item)]=0
            lists.setdata(data)
            await ctx.send('User Data Reset')
          except KeyError:
            await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
        else:
          return False
          
  @commands.command(name='balance',brief="Calls a user's balance.",help="Calls a member's balance. Just ping the user in the command. Format: n!balance @user")
  async def getuserloot(self,ctx,member: discord.Member):
    if str(ctx.message.author.id) not in banned:
      data = None
      print(member)
      #chk = lists.checkperms(ctx)
      gid = str(ctx.message.guild.id)
      lists.logback(ctx,member)
      #if chk == True:
      try:
        await ctx.send(dumps(lists.readdata()[gid][str(member)]).replace(':','=').replace('{','').replace('}','').replace('"',''))
      except KeyError:
        await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
    elif str(ctx.message.author.id) in banned:
      await ctx.send("Your ID Is In The Banned List.")
    else:
      await ctx.send("Error")

  @commands.command(name="addmember",brief="Adds a member to the clan's distribution database.", help="Adds a member to the distribution database. Just ping the user in the command. Format: n!addmember @User")
  async def addmember(self,ctx, member: discord.Member):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        lists.logback(ctx,member)
        inputv = {"flux":0,"loaders":0,"rcs":0,"pushers":0}
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        if chk == True:
          data[gid][str(member)]=dict(inputv)
          lists.setdata(data)
          await ctx.send(f'Added {member} to the distribution list in {ctx.message.guild.name}')
        else:
          return False

  @commands.command(name="removemember",brief="Removes a member from a clan's distribution database.", help="Removes a member from the distribution database. Just ping the user in the command and it will remove them. Format: n!removemember @User")
  async def remmem(self,ctx,member: discord.Member):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        mem=str(member)
        del data[gid][mem]
        lists.logback(ctx,member)
        if chk == True:
          try:
            lists.setdata(data)
            await ctx.send(f'Removed {member} from the distribution list in {msgparts[ctx.message.guild.name]}')
          except KeyError:
            await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
        else:
          return False

  @commands.command(name='balall',help="Calls all balances in a clan's distribution database. Format: n!balall")
  async def balanceall(self,ctx):
        clan = ctx.message.guild
        #msgparts, data = msg.split(" "), lists.readdata()
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        lists.logback(ctx,clan)
        mesg = str(gid)
        if chk == True:
          await ctx.send('Balances Of All Members')
          await ctx.send(dumps(lists.readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
        else:
          return False

  #@commands.Cog.listener()
  #async def on_message(self, ctx, msg):
    #msgparts, s1 = msg.split("\n")
    #print(s1)
    
def setup(bot: commands.Bot):
    bot.add_cog(DistCmds(bot))