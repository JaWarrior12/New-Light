import os, discord
import time
import pytz
import datetime 
#from keep_alive import keep_alive
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

class AdCmds(commands.Cog, name="Admin Tools", description="New Light Admin Tools"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    
  @commands.command(name="ban",hidden=True)
  @commands.has_role('Developer')
  async def banuser(self,ctx,user):
    if ctx.message.author.id in developers:
      keya = "all"
      keyb = "ban"
      gid=str(ctx.message.guild.id)
      data = dumps(lists.readdataE()[keyb])
      if str(user) in banned:
        await ctx.send(f'The User With An Id Of {user} Is Already In The Ban List')
      else:
        data = lists.readdataE()
        banlt=data
        #await ctx.send(banlt)
        banlt["ban"].append(str(user))
        #await ctx.send(banlt)
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
      gid =str(guild)
      data = dumps(lists.readdataE()[gid]["auth"])
      if str(user) in data:
        await ctx.send(f'The User With An Id Of {user} Is Already In The Ban List')
      else:
        data = lists.readdataE()
        banlt=data
        #await ctx.send(banlt)
        banlt[gid]["auth"].append(str(user))
        #await ctx.send(banlt)
        lists.setdataE(banlt)
        await ctx.send(f'The User With A User Id Of {user} has been Authorized.')
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
  async def leave(self, ctx,id, *, reason=None):
    if ctx.message.author.id in developers:
      guild = self.bot.get_guild(int(id))
      await ctx.send(guild.name)
      channel = discord.utils.get(guild.channels, name="general")
      await channel.send(f'My Developer Has Ordered Me To Leave Your Server. Reason My Developer Gave: {reason}. Please DM JaMinecrafter13#1305 if you have any questions or would like to add me back. You can also join my development server: https://discord.gg/zcGYBcfhwX')
      await guild.leave()
      await ctx.send(f':ok_hand: Left guild: {guild.name} ({guild.id})')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="clearserver",hidden=True)
  async def clearserver(self,ctx,id,*,reason=None):
    if ctx.message.author.id in developers:
      guild = self.bot.get_guild(int(id))
      channel = discord.utils.get(guild.channels, name="general")
      await channel.send(f'My Developer Has Ordered Me To Clear The Data For Your Server. Reason My Developer Gave: {reason}. Please DM JaMinecrafter13#1305 if you have any questions. You can also join my development server: https://discord.gg/zcGYBcfhwX')
      channel_id = channel.id
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
        await ctx.send(lines[int(min):int(max)])
      elif function=="backclr":
        with open("Backups/bcklog.txt", "w") as g:
          g.write(' ')
          await ctx.send("Cleared Backup Log")
      elif function=="disclr":
        with open("Backups/disconnectlogs.txt", "w") as g:
          g.write(' ')
          await ctx.send("Cleared Disconnect Log")
      elif function=="disr":
        with open("Backups/bcklog.txt", "r") as g:
          lines = g.readlines()
        await ctx.send(lines[int(min):int(max)])
      elif function=="bckr":
        with open("Backups/disconnectlogs.txt", "r") as g:
          lines = g.readlines()
        await ctx.send(lines[int(min):int(max)])
      else:
        await ctx.send("Error")
        return False
    else:
      await ctx.send("You are not a developer and cannot use this command.")

async def setup(bot: commands.Bot):
    await bot.add_cog(AdCmds(bot))