import os, discord
import time
import pytz
import datetime 
#from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get
from discord import app_commands
from discord import Member
from discord import Permissions
from json import loads, dumps
from backup import backup
from startup import startup
import lists

banned= lists.banned


class SetupCmds(commands.Cog, name="Server Commands",description="Server Setup Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name="setupserver",brief="Setup For Your Server",help="Sets Up Databases and Configs For Your Server. ONLY RUN THIS ONCE!!! Administrator Permissions are required to run this command. It automaticlly adds the person who ran the command to the authorized users list. Ping Channel is for the NL Ping Webpage, simply insert the CHANNEL ID of your Battle Links channel.")
  @commands.has_permissions(administrator=True)
  async def setupsrvr(self,ctx,pingChannel=None,distroChannel=None):
      servers=lists.readdata()
      if str(ctx.message.guild.id) not in servers.keys():
        msg = None
        lists.logback(ctx,msg)
        msgb = "a b"
        pc=int(pingChannel)
        gid = ctx.message.guild.id
        uid = ctx.message.author.id
        #await lists.logmajor(self,ctx,msg=str(uid))
        default = {}
        defaultb=[]
        defaultc={"auth":[],"pingchan":pc,"distchan":int(distroChannel)}
        data = lists.readdata()
        data[gid]=dict(default)
        lists.setdata(data)
        data = lists.readdataB()
        data[gid]=dict(default)
        lists.setdataB(data)
        data = lists.readdataC()
        data[gid]=defaultb
        lists.setdataC(data)
        data = lists.readdataD()
        data[gid]=dict(default)
        lists.setdataD(data)
        data = lists.readdataE()
        data[gid]=dict(defaultc)
        lists.setdataE(data)
        data = lists.readdataE()
        banlt=data
        banlt[gid]["auth"].append(str(uid))
        lists.setdataE(banlt)
        server = ctx.message.guild
        await server.create_role(name="QuickPing")
      else:
        await ctx.send("Server already setup.")

  @commands.command(name="authuser",help="Authorizes A User To Use Leadership Commands. Required Permissions: Administrator; Format: n!authuser <USERID>")
  @commands.has_permissions(administrator=True)
  async def authorizeuser(self,ctx,user):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      if chk == True:
        #await lists.logmajor(ctx,user)
        #lists.logmajor(self,ctx,user)
        gid=str(ctx.message.guild.id)
        key="auth"
        data = dumps(lists.readdataE()[gid][key])
        if str(user) in data:
          await ctx.send(f'The User With An ID Of {user} Is Already Authorized')
        else:
          data = lists.readdataE()
          banlt=data
          #await ctx.send(banlt)
          banlt[gid]["auth"].append(str(user))
          #await ctx.send(banlt)
          lists.setdataE(banlt)
          await ctx.send(f'The User With A User Id Of {user} has been authorized to use Leadership Commands in the server {ctx.message.guild.name} by {ctx.message.author.name}')
          myguild = ctx.guild
          channel = myguild.get_channel(1037788623015268444)
          e = discord.Embed(title="User Authorized")
          e.add_field(name="Server Name", value=ctx.guild.name, inline=False)
          e.add_field(name="Server ID", value=ctx.guild.id, inline=False)
          e.add_field(name="User Authorizing", value=f'Name:{ctx.message.author.name}; ID:{ctx.message.author.id}', inline=False)
          member=ctx.guild.get_member(int(user))
          e.add_field(name="User Being Authorized", value=f'Name:{member.name}; ID:{member.id}', inline=False)
          tz = pytz.timezone('America/New_York')
          e.timestamp=datetime.datetime.now(tz)
          await channel.send(embed=e)
          
      else:
        await ctx.send("You are not authorized and CANNOT authorize users.")
    elif str(ctx.messsage.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    else:
      await ctx.send("I Hit a Wall, Try Running The Command Again")

  def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)
  
  @commands.command(name="deauthuser",help="Removes Authorization From A User To Use Leadership Commands. Required Permissions: Administrator; Format: n!deauthuser <USERID>")
  @commands.check_any(is_guild_owner())
  async def deathuser(self,ctx,user):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      if chk == True:
        #await lists.logmajor(ctx,user)
        #lists.logmajor(self,ctx,user)
        gid=str(ctx.message.guild.id)
        key="auth"
        data = dumps(lists.readdataE()[gid][key])
        if str(user) not in data:
          await ctx.send(f'The User With An ID Of {user} Is Not Authorized')
        else:
          data = lists.readdataE()
          banlt=data
          #await ctx.send(banlt)
          banlt[gid]["auth"].remove(str(user))
          #await ctx.send(banlt)
          lists.setdataE(banlt)
          await ctx.send(f'The User With A User Id Of {user} has been DEAUTHORIZED to use Leadership Commands in the server {ctx.message.guild.name} by {ctx.message.author.name}')
          myguild = ctx.guild
          channel = myguild.get_channel(1037788623015268444)
          e = discord.Embed(title="User Deauthorized")
          e.add_field(name="Server Name", value=ctx.guild.name, inline=False)
          e.add_field(name="Server ID", value=ctx.guild.id, inline=False)
          e.add_field(name="User Deauhtorizing", value=f'Name:{ctx.message.author.name}; ID:{ctx.message.author.id}', inline=False)
          member=ctx.guild.get_member(int(user))
          e.add_field(name="User Being Deauthorized", value=f'Name:{member.name}; ID:{member.id}', inline=False)
          tz = pytz.timezone('America/New_York')
          e.timestamp=datetime.datetime.now(tz)
          await channel.send(embed=e)
          
      else:
        await ctx.send("You are not authorized and CANNOT authorize users.")
    elif str(ctx.messsage.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    else:
      await ctx.send("I Hit a Wall, Try Running The Command Again")

  @commands.command(name="authlist",description="Lists all users authorized to use leadership commands in the server.")
  async def authlist(self,ctx):
    if str(ctx.message.author.id) not in banned:
      msg="none"
      msgb = str(msg)
      chk = lists.checkperms(ctx)
      gid = str(ctx.message.guild.id)
      lists.logback(ctx,msgb)
      list=lists.readdataE()
      if chk == True:
        for mem in list[str(ctx.message.guild.id)]["auth"]:
          member=ctx.message.guild.get_member(int(mem))
          await ctx.send(f'Name:{member.display_name}; ID:{member.id}')
    else:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')

async def setup(bot: commands.Bot):
    await bot.add_cog(SetupCmds(bot))