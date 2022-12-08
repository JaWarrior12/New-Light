import os, discord
import time
import pytz
import datetime 
from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get
from discord import Member
from discord import Permissions
from json import loads, dumps
from backup import backup
from startup import startup

#Lists
import lists
#import main
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

class AdCmds(commands.Cog, name="Admin Tools"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    
  @commands.command(name="ban",hidden=True)
  @commands.has_role('Developer')
  async def banuser(self,ctx,user):
    if ctx.message.author.id in developers:
      keya = "all"
      keyb = "ban"
      gid = str(ctx.message.guild.id)
      data = dumps(lists.readdataE()[keyb])
      if str(user) in banned:
        await ctx.send(f'The User With An Id Of {user} Is Already In The Ban List')
      else:
        data = lists.readdataE()
        banlt=data
        await ctx.send(banlt)
        banlt["ban"].append(str(user))
        await ctx.send(banlt)
        lists.setdataE(banlt)
        await ctx.send(f'The User With A User Id Of {user} has been BANNED from using New Light')
        lists.bannedlist()
    else:
      await ctx.send("You are not a developer and cannot use this command")

  @commands.command(name="unban",hidden=True)
  async def unban(self,ctx,user_id):
    if ctx.message.author.id in developers:
      if str(user_id) not in banned:
        await ctx.send(f'The User With An ID Of {user_id} Is Not In The Banned List.')
      elif str(user_id) in banned:
        data = lists.readdataE()
        banlt=data
        #await ctx.send(banlt)
        banlt["ban"].remove(str(user_id))
        #await ctx.send(banlt)
        lists.setdataE(banlt)
        lists.bannedlist()
        await ctx.send(f'The User With An ID Of {user_id} Has Been Unbanned From Using New Light')
      else:
        await ctx.send(f'The ID of {user_id} could not be found, try again.')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="deauth",hidden=True)
  async def deauth(self,ctx,guild,user):
    if ctx.message.author.id in developers:
      data=lists.readdataE()
      authlt=data#[str(guild)]["auth"]
      #await ctx.send(authlt)
      authlt[str(guild)]["auth"].remove(str(user))
      #await ctx.send(authlt)
      lists.setdataE(authlt)
      await ctx.send(f'User With An ID Of {user} has been deauthorized in the guild with an id of {guild}.')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="authus",hidden=True)
  async def authus(self,ctx,guild,user):
    if ctx.message.author.id in developers:
      data=lists.readdataE()
      authlt=data#[str(guild)]["auth"]
      #await ctx.send(authlt)
      authlt[str(guild)]["auth"].extend(str(user))
      #await ctx.send(authlt)
      lists.setdataE(authlt)
      await ctx.send(f'User With An ID Of {user} has been deauthorized in the guild with an id of {guild}.')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="listguilds",hidden=True)
  async def listguilds(self,ctx):
    if ctx.message.author.id in developers:
      names=[]
      ids=[]
      for guild in self.bot.guilds:
        names.append(guild.name)
        ids.append(guild.id)
      await ctx.send(names)
      await ctx.send(ids)
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="leaveserver",hidden=True)
  async def leave(self, ctx, *, guild_name):
    if ctx.message.author.id in developers:
      guild = discord.utils.get(self.bot.guilds, name=guild_name)
      if guild is None:
          await ctx.send("I don't recognize that guild.")
          return
      await self.bot.leave_guild(guild)
      await ctx.send(f":ok_hand: Left guild: {guild.name} ({guild.id})")
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="clearserver",hidden=True)
  async def clearserver(self,ctx,id):
    if ctx.message.author.id in developers:
      gid=str(id)
      data=lists.readdata()
      data.pop(gid)
      lists.setdata(data)
      gid=str(id)
      data=lists.readdataB()
      data.pop(gid)
      lists.setdataB(data)
      gid=str(id)
      data=lists.readdataC()
      data.pop(gid)
      lists.setdataC(data)
      gid=str(id)
      data=lists.readdataD()
      data.pop(gid)
      lists.setdataD(data)
      gid=str(id)
      data=lists.readdataE()
      data.pop(gid)
      lists.setdataE(data)
      await ctx.send(f'The server with an ID of {gid} has been removed from my databases.')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="authedus",hidden=True)
  async def authedus(self,ctx,guild=None):
    if ctx.message.author.id in developers:
      data=lists.readdataE()
      if guild==None:
        await ctx.send(data)
      elif guild!=None:
        gid=str(guild)
        await ctx.send(data[gid]["auth"])
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="logdat",hidden=True)
  async def logdat(self,ctx,function,min=None,max=None):
    if ctx.message.author.id in developers:
      if function=="clear":
        with open("Backups/log.txt", "w") as g:
          g.write(' ')
          await ctx.send("Cleared Command Log")
      elif function=="read":
        with open("Backups/log.txt", "r") as g:
          lines = g.readlines()
        await ctx.send(lines[min:max])
      else:
        await ctx.send("Error")
        return False
    else:
      await ctx.send("You are not a developer and cannot use this command.")

def setup(bot: commands.Bot):
    bot.add_cog(AdCmds(bot))