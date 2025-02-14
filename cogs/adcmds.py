import os
import discord
import time
import pytz
import sys
import datetime
from datetime import time as DT_time
from typing import List
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
      global banned
      try:
        user=int(user)
      except:
        return "Not A Valid Integer"
      keya = "all"
      keyb = "ban"
      gid=str(ctx.message.guild.id)
      lists.bannedlist()
      data = dumps(lists.readFile("config"))
      if type(user) is discord.Member:
            baseUser=user
            user=user.id
            #name=user.display
      else:
        user=user
      if str(user) in banned:
        await ctx.send(f'The User With An Id Of {user} Is Already In The Ban List')
      elif type(user)==int:
        data = lists.readFile("config")
        banlt=data
        banlt["ban"].append(str(user))
        other=lists.readFile("other")
        tz = pytz.timezone('America/New_York')
        date=f"{datetime.datetime.now(tz).month}-{datetime.datetime.now(tz).day}-{datetime.datetime.now(tz).year}"
        try:
          userObject=await self.bot.fetch_user(int(user))
          other["banInfo"].update({str(userObject.id):{"reason":reason,"userName":userObject.name,"banDate":date}})
        except:
          other["banInfo"].update({str(user):{"reason":reason,"userName":None,"banDate":date}})
        lists.setFile("other",other)
        lists.setFile("config",banlt)
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
      lists.bannedlist()
      if str(user_id) not in banned:
        await ctx.send(f'The User With An ID Of {user_id} Is Not In The Banned List.')
      elif type(user_id)==int:
        await ctx.send(f"User ID `{user_id}` isn't and integer! It needs to be an integer!")
      elif str(user_id) in banned and type(user_id)==str:
        data = lists.readFile("config")
        banlt=data
        banlt["ban"].remove(str(user_id))
        other=lists.readFile("other")
        lists.setFile("other",other)
        lists.setFile("config",banlt)
        lists.bannedlist()
        await ctx.send(f'The User With An ID Of {user_id} Has Been Unbanned From Using New Light')
      else:
        await ctx.send(f'The ID of {user_id} could not be found, try again.')
    else:
      await ctx.send("You are not a developer and cannot use this command.")

  @commands.command(name="banguild",help="Bans A Server From Using New Light")
  async def banguild(self,ctx,gid,*,reason=None):
    if ctx.message.author.id in developers:
      if type(gid)==str:
        data=lists.readdataE()
        data["banguilds"].append(int(gid))
        other=lists.readother()
        tz = pytz.timezone('America/New_York')
        date=date=f"{datetime.datetime.now(tz).month}-{datetime.datetime.now(tz).day}-{datetime.datetime.now(tz).year}"
        try:
          guild=await self.bot.fetch_guild(gid)
          other["banInfo"].update({str(gid):{"reason":reason,"guildName":guild.name,"banDate":date}})
        except:
          other["banInfo"].update({str(gid):{"reason":reason,"guildName":None,"banDate":date}})
        #print(other)
        try:
          lists.setother(other)
        except Exception as e:
          pass
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
      try:
        if type(gid)!=int:
          lists.bannedguilds()
          data=lists.readFile("config")
          data["banguilds"].remove(int(gid))
          other=lists.readFile("other")
          try:
            guild=await self.bot.fetch_guild(gid)
          except:
            pass
          await ctx.send(f"Guild Ban Info: {other["banInfo"][str(gid)]}")
          other["banInfo"].pop(str(gid))
          lists.setFile("other",other)
          lists.setFile("config",data)
          lists.bannedguilds()
          await ctx.send(f"UnBanned Guild With ID:{gid}")
        else:
          await ctx.send(f"Guild ID `{gid}` isn't an integer! It Needs to be an integer!")
      except Exception as e:
        print(e)
    else:
      await ctx.send("Not A Dev")

  @commands.command(name="banlist",help="Lists Banned Guilds or Users",description="Opt can be `users` for users or `guilds` for guilds.")
  async def  banlist(self,ctx,opt):
    if ctx.message.author.id in developers:
      if opt=="users":
        data=lists.readFile("config")
        other=lists.readFile("other")["banInfo"]
        ctnt=""
        for x in data["ban"]:
          try:
            if "userName" in list(other[str(x)].keys()):
              ctnt=ctnt+"\n- "+str(x)+f" ; User Name: `{other[str(x)]['userName']}` ; Ban Reason: `{other[str(x)]['reason']}` ; Ban Date: {other[str(x)]['banDate']}"
            else:
              pass
          except Exception as e:
            print(e)
        await ctx.send(f'Banned Users:\n{ctnt}')
      elif opt=="guilds":
        try:
          data=lists.readFile("config")
          other=lists.readFile("other")["banInfo"]
          ctnt=""
          guilds=[]
          for x in other.keys():
            if "guildName" in other[str(x)].keys():
              if int(x) in data["banguilds"]:
                guilds.append(int(x))
          for y in guilds:
            guildData="\n-"+f" {str(y)} ; Guild Name: `{other[str(y)]['guildName']}` ; Ban Reason: `{other[str(y)]['reason']}` ; Ban Date: {other[str(y)]['banDate']}"
            ctnt=ctnt+guildData
          await ctx.send(f'Banned Guilds:\n{ctnt}')
        except Exception as e:
          pass
      else:
        await ctx.send("I don't know what you want me to list.")
    else:
      await ctx.send("Not A Dev")

  @commands.command(name="deauth",hidden=False,help="Remotely Deauthorizes a user in a server.")
  async def deauth(self,ctx,guild,user):
    if ctx.message.author.id in developers:
      data=lists.readFile("config")
      authlt=data
      authlt[str(guild)]["auth"].remove(str(user))
      lists.setFile("config",authlt)
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
        data = lists.readFile("config")
        banlt=data
        banlt[gid]["auth"].append(str(user))
        lists.setFile("config",banlt)
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
      data=lists.readFile("distribution")
      data.pop(gid)
      lists.setFile("distribution",data)
      gid=str(id)
      data=lists.readFile("relations")
      data.pop(gid)
      lists.setFile("relations",data)
      gid=str(id)
      data=lists.readFile("quickping")
      data.pop(gid)
      lists.setFile("quickping",data)
      gid=str(id)
      data=lists.readFile("designs")
      data.pop(gid)
      lists.setFile("designs",data)
      gid=str(id)
      data=lists.readFile("config")
      data.pop(gid)
      lists.setFile("config",data)
      data=lists.readFile("other")
      data["defaultdist"].pop(gid)
      lists.setFile("other",data)
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
      kys=list(lists.readFile("config").keys())
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
      data=lists.readFile("config")
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

  @commands.command(name="remoteServerSettings",aliases=["rss","remoteChange"],help="Allows remote management of a server's settings by the developer.")
  async def remoteServerSettings(self,ctx,guildID,option,*,input):
    if ctx.message.author.id in developers:
      guild=self.bot.get_guild(int(guildID))
      val = 0
      val=input
      if option == "distship":
        val=str(input)
      elif option=="clanPercent":
        val=float(input)
      elif option in ["verbal","logFiltersNonShips"]:
        val=bool(input)
      elif option == "storebal":
        val=str(input.lower())
      else:
        val=int(input)
      opt=option
      print(opt)          
      data=lists.readFile("config")
      prevVal=data[str(guild.id)][opt]
      data[str(guild.id)][opt]=val
      lists.setFile("config",data)
      await ctx.send(f'Changed {(option)} in `{guild.name} ({guild.id})` from {prevVal} to {val}')
      guildOwner=guild.owner
      await guild.Owner.send(f'{ctx.message.author.name} has remotely changed {(option)} in `{guild.name} ({guild.id})` from {prevVal} to {val}')
    else:
      await ctx.send("Sorry, only developers can use this command.")

  @commands.command(name="remoteCheckPerms",aliases=["rcp","remotePerms"],help="Allows the developer to remotely check the perms New Light has in a server. Primarally used for troubleshooting without needing to give the dev perms.")
  async def remoteCheckPerms(self,ctx,guildID):
    if ctx.message.author.id in developers:
      guild=self.bot.get_guild(int(guildID))
      outputFileName=f"{guild.name}_perms_list.md"
      outputFile=None
      try:
        with open(outputFileName, "a+", encoding="utf-8") as outputFile:
          outputFile.write(f"# Server: {guild.name} ({guild.id})\n")
          for channel in guild.channels:
            outputFile.write(f"- Channel: {channel.name} ({channel.id})\n")
            permsList=[perm for perm in channel.permissions_for(guild.get_member(self.bot.application_id))]
            for perm in permsList:
              outputFile.write(f" - Permission: `{perm[0]}`; Value: `{perm[1]}`\n")
        await ctx.send(f"{guild.name} Perms List:",file=discord.File(outputFileName))
        os.remove(outputFileName)
      except Exception as e:
        print(e)
        os.remove(outputFileName)
    else:
      await ctx.send("Sorry, only developers can use this command.")

async def setup(bot: commands.Bot):
    await bot.add_cog(AdCmds(bot))