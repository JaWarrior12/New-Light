import os
import discord
import time
import pytz
import datetime
from datetime import time as DT_time
from typing import List
#from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.utils import get
from discord import Member
from discord import Permissions
from discord import app_commands
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

class AdCmds(commands.Cog, name="Dev Admin Tools", description="New Light Developer Admin Tools"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.syncBanlists.start()
  def cog_unload(self):
    self.syncBanlists.cancel()
  
    
    
  @commands.command(name="ban",hidden=False,help="Bans A User From Using New Light")
  #@commands.has_role('Developer')
  async def banuser(self,ctx,user,*,reason=None):
    if ctx.message.author.id in developers:
      try:
        user=int(user)
      except:
        return "Not A Valid Integer"
      keya = "all"
      keyb = "ban"
      gid=str(ctx.message.guild.id)
      data = dumps(lists.readdataE())
      print(type(user))
      if type(user) is discord.Member:
            baseUser=user
            user=user.id
            #name=user.display
      else:
        user=user
      if str(user) in banned:
        await ctx.send(f'The User With An Id Of {user} Is Already In The Ban List')
      elif type(user)==int:
        #print("int")
        data = lists.readdataE()
        banlt=data
        #await ctx.send(banlt)
        banlt["ban"].append(str(user))
        #print(banlt)
        #await ctx.send(banlt)
        other=lists.readother()
        #print(1)
        tz = pytz.timezone('America/New_York')
        #print(tz)
        date=datetime.datetime.today()
        #print(date)
        try:
          userObject=await self.bot.fetch_user(int(user))
          #print(userObject)
          other["banInfo"].update({str(userObject.id):{"reason":reason,"name":userObject.name,"banDate":date}})
        except:
          #print("other")
          other["banInfo"].update({str(user):{"reason":reason,"name":None,"banDate":date}})
        lists.setdataE(banlt)
        await ctx.send(f'The User With A User Id Of {user} has been BANNED from using New Light')
        lists.bannedlist()
        banned=banlt["ban"]
      elif type(user) != int:
        await ctx.send(f"Error! User `{user}` is not an integer, and therefore not an ID!")
      else:
        await ctx.send("Unknown Error!")
    else:
      await ctx.send("You are not a developer and cannot use this command")

  @commands.command(name="unban",hidden=False,help="Unbans A User From Using New Light")
  async def unban(self,ctx,user_id):
    if ctx.message.author.id in developers:
      if str(user_id) not in banned:
        await ctx.send(f'The User With An ID Of {user_id} Is Not In The Banned List.')
      elif type(user_id)==int:
        await ctx.send(f"User ID `{user_id}` isn't and integer! It needs to be an integer!")
      elif str(user_id) in banned and type(user_id)==str:
        data = lists.readdataE()
        banlt=data
        #await ctx.send(banlt)
        banlt["ban"].remove(str(user_id))
        other=lists.readother()
        other["banInfo"].pop(str(user_id))
        lists.setother(other)
        #await ctx.send(banlt)
        lists.setdataE(banlt)
        lists.bannedlist()
        await ctx.send(f'The User With An ID Of {user_id} Has Been Unbanned From Using New Light')
      else:
        await ctx.send(f'The ID of {user_id} could not be found, try again.')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="banguild",help="Bans A Server From Using New Light")
  async def banguild(self,ctx,gid,*,reason=None):
    if ctx.message.author.id in developers:
      if type(gid)==int:
        data=lists.readdataE()
        data["banguilds"].append(int(gid))
        other=lists.readother()
        guild=await self.bot.fetch_guild(gid)
        tz = pytz.timezone('America/New_York')
        date=datetime.now(tz)
        try:
          other["banInfo"].update({str(gid):{"reason":reason,"name":guild.name,"banDate":date}})
        except:
          other["banInfo"].update({str(gid):{"reason":reason,"name":None,"banDate":date}})
        lists.setother(other)
        lists.setdataE(data)
        lists.bannedguilds()
        await ctx.send(f"Banned Guild With ID:{gid}")
      else:
        await ctx.send(f"Guild ID `{gid}` isn't an integer! It must be an integer!")
    else:
      await ctx.send("Not A Dev")

  @commands.command(name="unbanguild",help="Unbans A Server From Using New Light")
  async def unbanguild(self,ctx,gid,*,reason=None):
    if ctx.message.author.id in developers:
      if type(gid)!=int:
        data=lists.readdataE()
        data["banguilds"].remove(int(gid))
        lists.setdataE(data)
        other=lists.readother()
        guild=await self.bot.fetch_guild(gid)
        other["banInfo"].pop(str(gid))
        lists.setother(other)
        lists.bannedguilds()
        await ctx.send(f"UnBanned Guild With ID:{gid}")
      else:
        await ctx.send(f"Guild ID `{gid}` isn't an integer! It Needs to be an integer!")
    else:
      await ctx.send("Not A Dev")

  @commands.command(name="banlist",help="Lists Banned Guilds or Users",description="Opt can be `users` for users or `guilds` for guilds.")
  async def  banlist(self,ctx,opt):
    if ctx.message.author.id in developers:
      if opt=="users":
        data=lists.readdataE()
        other=lists.readother()["banInfo"]
        ctnt=""
        for x in data["ban"]:
          #print(x)
          try:
            ctnt=ctnt+"\n-"+str(x)+f" ; User Name: `{other[str(x)]['name']}` ; Ban Reason: `{other[str(x)]['reason']}` ; Ban Date: {other[str(x)]['date']}"
          except Exception as e:
            await ctx.send(e)
          #print(ctnt)
        await ctx.send(f'Banned Users:\n{ctnt}')
      elif opt=="guilds":
        data=lists.readdataE()
        ctnt=""
        for x in data["banguilds"]:
          ctnt=ctnt+"\n-"+str(x)+f" ; User Name: `{other[str(x)]['name']}` ; Ban Reason: `{other[str(x)]['reason']}` ; Ban Date: {other[str(x)['banDate']]}"
        await ctx.send(f'Banned Guilds:\n{ctnt}')
      else:
        await ctx.send("I don't know what you want me to list.")
    else:
      await ctx.send("Not A Dev")

  @commands.command(name="deauth",hidden=False,help="Remotely Deauthorizes a user in a server.")
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

  @commands.command(name="authus",hidden=False,help="Remotely Authorizes A User In A Server")
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

  @commands.command(name="listguilds",hidden=False,help="Lists All Servers New Light Is In")
  async def listguilds(self,ctx):
    if ctx.message.author.id in developers:
      names=[]
      ids=[]
      for guild in self.bot.guilds:
        await ctx.send(f'Name:{guild.name}')
        await ctx.send(f'ID:{guild.id}\n')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="leaveserver",hidden=False,help="Forces New Light To Leave A Server")
  async def leave(self, ctx,id, *, reason=None):
    if ctx.message.author.id in developers:
      guild = self.bot.get_guild(int(id))
      await ctx.send(guild.name)
      channel = guild.system_channel
      await guild.system_channel.send(f'My Developer Has Ordered Me To Leave Your Server. Reason: {reason}. Please DM JaWarrior#1305 if you have any questions or would like to add me back. You can also join my development server: https://discord.gg/zcGYBcfhwX')
      await guild.leave()
      await ctx.send(f':ok_hand: Left guild: {guild.name} ({guild.id})')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="clearserver",hidden=False,help="Clears A Server From New Light's Databases")
  async def clearserver(self,ctx,id,*,reason=None):
    if ctx.message.author.id in developers:
      guild = self.bot.get_guild(int(id))
      channel = guild.system_channel
      await guild.system_channel.send(f'My Developer Has Ordered Me To Clear The Data For Your Server. Reason: {reason}. Please DM JaWarrior#1305 if you have any questions. You can also join my development server: https://discord.gg/zcGYBcfhwX')
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
      data=lists.readother()
      data["defaultdist"].pop(gid)
      lists.setother(data)
      await ctx.send(f'The server with an ID of {gid} has been removed from my databases.')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="clearold",help="Removes Servers NL Is No Longer In From Databases")
  async def clearold(self,ctx):
    if ctx.message.author.id in developers:
      await ctx.send("Clearing Guilds")
      myguilds=[]
      for y in self.bot.guilds:
        myguilds.append(str(y.id))
      kys=list(lists.readdataE().keys())
      myguilds.append("ban")
      myguilds.append("banguilds")
      kys=kys
      for z in myguilds:
        if z in kys:
          kys.remove(z)
        else:
          pass
      kysb=kys
      await ctx.send(f'Cleaing The Following Guilds: {kysb}')
      for x in kysb:
          lists.clearserver(str(x))
      await ctx.send("Cleared Empty Guilds")
    else:
      pass

  @commands.command(name="authedus",hidden=False,help="Lists Authorized Users in a guild")
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

  @commands.command(name="logdat",hidden=False,help="Reads Log Data")
  async def logdat(self,ctx,function,min=10,max=10):
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
      elif function=="bckr":
        with open("Backups/bcklog.txt", "r") as g:
          lines = g.readlines()
        await ctx.send(lines[int(min):int(max)])
      elif function=="disr":
        with open("Backups/disconnectlogs.txt", "r") as g:
          lines = g.readlines()
        await ctx.send(lines[int(min):int(max)])
      else:
        await ctx.send("Error")
        return False
    else:
      await ctx.send("You are not a developer and cannot use this command.")
      pass

  @commands.command(name="createinvite",hidden=False,help="Creates An Invite For The Developer")
  async def createinvite(self,ctx,gid):
    if int(ctx.message.author.id) in developers:
      guild = self.bot.get_guild(int(gid))
      invite=None
      if guild.system_channel==None:
        invite="No System Channel Found, Unable To Create Invite"
      else:
        invite = await guild.system_channel.create_invite(reason="My Developer Has Requested An Invite")
      await ctx.send(invite)
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @tasks.loop(hours=1)
  async def syncBanlists(self):
    lists.bannedlist()
    lists.bannedguilds()
    
async def setup(bot: commands.Bot):
    await bot.add_cog(AdCmds(bot))