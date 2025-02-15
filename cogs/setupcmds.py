from ast import alias
import os
from pdb import run
import sys
import discord
import time
import pytz
import datetime
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from discord import Member
from discord import Permissions
from json import loads, dumps
from backup import backup
from startup import startup
import lists

banned=lists.banned
developers=lists.developers

FILTERED_ROLES=["Founder / Damage control"]
CONTAINS_ROLE_FILTER=["admin","administrator","administration","perms","moderation","moderator"]

class SetupCmds(commands.Cog, name="Server Commands",description="Server Setup Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    if self.bot.user.id == 974045822167679087:
      self.runUpdateMemList.start()
  def cog_unload(self):
    if self.bot.user.id == 974045822167679087:
      self.runUpdateMemList.cancel()

  def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id or ctx.author.id in lists.developers
    return commands.check(predicate)

  @commands.command(name="setupserver",aliases=["setup","serversetup"],brief="Setup For Your Server (Server Owner Only)",help="Sets Up Databases and Configs For Your Server. ONLY RUN THIS ONCE!!! Administrator Permissions are required to run this command. It automaticlly adds the person who ran the command to the authorized users list. If server owner is unavailable, contact jawarrior about continuing setup.")
  #@commands.has_permissions(administrator=True)
  @commands.check_any(is_guild_owner())
  async def setupsrvr(self,ctx):
      servers=lists.readdataE()
      if str(ctx.message.guild.id) not in servers.keys():
        try:
          await ctx.send("Started Server Setup")
          msg = None
          msgb = "a b"
          gid = ctx.message.guild.id
          uid = ctx.message.author.id
          default = {}
          defaultb=[]
          defaultc={"auth":[str(uid)],"pingchan":0,"distchan":0,"clanPercent":0,"distship":0,"memrole":0,"storebal":"no","name":str(ctx.message.guild.name),"memchan":0,"memmsg":0,"verbal":False,"nonverProof":False,"trackLogChannel":0,"logFiltersNonShips":True,"inventoryLogChannel":0,"translationBool":False}
          defaultd={"clan":{"flux":0,"iron":0,"explosive":0,"cannon":0,"burst_cannon":0,"machine_cannon":0,"loader":0,"pusher":0,"rubber":0,"handheld":0,"ice":0,"item_launcher":0,"rcd":0}}
          data = lists.readFile("distribution")
          data[gid]=dict(defaultd)
          lists.setFile("distribution",data)
          data = lists.readFile("relations")
          data[gid]=defaultb
          lists.setFile("relations",data)
          data = lists.readFile("quickping")
          data[gid]=default
          lists.setFile("quickping",data)
          data = lists.readFile("designs")
          data[gid]=dict(default)
          lists.setFile("designs",data)
          data = lists.readFile("config")
          data[gid]=dict(defaultc)
          lists.setFile("config",data)
          data = lists.readFile("dailyReportsConfig")
          data[gid]={"trackList":[],"inventoryList":[]}
          lists.setFile("dailyReportsConfig",data)
          data = lists.readFile("translationConfid")
          data[gid]={"langChannels":[]}
          lists.setFile("translationConfig",data)
          await ctx.send("Server Setup Succesfully!")
          #await server.create_role(name="QuickPing")
          #await ctx.send("QuickPing Role Created")
        except Exception as e:
          print(e)
          await ctx.send("Server Setup Succesfully!")
      else:
        await ctx.send("Server already setup.")

  @commands.command(name="authuser",breif="Authorizes User For LR Commands (LR)",help="Authorizes A User To Use Leadership Commands. Required Permissions: Administrator; Format: n!authuser <USERID>")
  #@commands.has_permissions(administrator=True)
  @commands.check_any(is_guild_owner())
  async def authorizeuser(self,ctx,user:discord.Member):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      if chk == True:
        gid=str(ctx.message.guild.id)
        key="auth"
        data = dumps(lists.readFile("config")[gid][key])
        if str(user.id) in data:
          await ctx.send(f'{user.mention} Is Already Authorized')
        else:
          data = lists.readFile("config")
          banlt=data
          banlt[gid]["auth"].append(str(user.id))
          lists.setFile("config",banlt)
          await ctx.send(f'{user.mention} has been authorized to use Leadership Commands in the server {ctx.message.guild.name} by {ctx.message.author.name}')
          myguild = ctx.guild
          channel = myguild.get_channel(1037788623015268444)
          e = discord.Embed(title="User Authorized")
          e.add_field(name="Server Name", value=ctx.guild.name, inline=False)
          e.add_field(name="Server ID", value=ctx.guild.id, inline=False)
          e.add_field(name="User Authorizing", value=f'Name:{ctx.message.author.name}; ID:{ctx.message.author.id}', inline=False)
          e.add_field(name="User Being Authorized", value=f'Name:{user.display_name}; ID:{user.id}', inline=False)
          tz = pytz.timezone('America/New_York')
          e.timestamp=datetime.datetime.now(tz)
          await channel.send(embed=e)
          
      else:
        await ctx.send("You are not authorized and CANNOT authorize users.")
    elif str(ctx.messsage.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    else:
      await ctx.send("I Hit a Wall, Try Running The Command Again")

  
  @commands.command(name="deauthuser",brief="Removes a user's LR access. (LR)",help="Removes Authorization From A User To Use Leadership Commands. Required Permissions: Administrator; Format: n!deauthuser @user")
  @commands.check_any(is_guild_owner())
  async def deathuser(self,ctx,user: discord.Member):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      if chk == True:
        gid=str(ctx.message.guild.id)
        key="auth"
        data = dumps(lists.readFile("config")[gid][key])
        if str(user) not in data:
          await ctx.send(f'{user.mention} Is Not Authorized')
        else:
          data = lists.readFile("config")
          banlt=data
          banlt[gid]["auth"].remove(str(user.id))
          lists.setFile("config",banlt)
          await ctx.send(f'{user.mention} has been DEAUTHORIZED to use Leadership Commands in the server {ctx.message.guild.name} by {ctx.message.author.name}')
          myguild = ctx.guild
          channel = myguild.get_channel(1037788623015268444)
          e = discord.Embed(title="User Deauthorized")
          e.add_field(name="Server Name", value=ctx.guild.name, inline=False)
          e.add_field(name="Server ID", value=ctx.guild.id, inline=False)
          e.add_field(name="User Deauhtorizing", value=f'Name:{ctx.message.author.name}; ID:{ctx.message.author.id}', inline=False)
          e.add_field(name="User Being Deauthorized", value=f'Name:{user.display_name}; ID:{user.id}', inline=False)
          tz = pytz.timezone('America/New_York')
          e.timestamp=datetime.datetime.now(tz)
          await channel.send(embed=e)
          
      else:
        await ctx.send("You are not authorized and CANNOT authorize users.")
    elif str(ctx.messsage.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    else:
      await ctx.send("I Hit a Wall, Try Running The Command Again")

  @commands.command(name="authlist",brief="Gets Servers LR Authorized List (Server Owner Only)",help="Lists all users authorized to use leadership commands in the server.")
  @commands.check_any(is_guild_owner())
  async def authlist(self,ctx):
    if str(ctx.message.author.id) not in banned:
      msg="none"
      msgb = str(msg)
      chk = lists.checkperms(ctx)
      gid = str(ctx.message.guild.id)
      list=lists.readFile("config")
      if chk == True:
        for mem in list[str(ctx.message.guild.id)]["auth"]:
          member=ctx.message.guild.get_member(int(mem))
          await ctx.send(f'Name:{member.display_name}; ID:{member.id}')
    else:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
      
  @commands.command(name="confighelp",help="Description of ServerConfig Settings")
  async def conhelp(self,ctx):
    await ctx.send("Please See The Wiki Page: https://github.com/JaWarrior12/New-Light/wiki/Setup-Guide#config-settings")

  @app_commands.command(name="serverconfig",description="Server Config (LR), n!confighelp for help")
  #@app_commands.checks.has_permissions(administrator=True)
  @app_commands.choices(option=[
      app_commands.Choice(name="Ping Channel", value="pingchan"),
      app_commands.Choice(name="Distribution Channel", value="distchan"),
      app_commands.Choice(name="Clan Percent",value="clanPercent"),
      app_commands.Choice(name="Clan Storage (Hexcode)",value="distship"),
      app_commands.Choice(name="Member Role",value="memrole"),
      app_commands.Choice(name="Store Member Balances? (Yes/No)",value="storebal"),
      app_commands.Choice(name="Member List Channel",value="memchan"),
      app_commands.Choice(name="Verify Distribution Logs?",value="verbal"),
      app_commands.Choice(name="Track Log Channel",value="trackLogChannel"),
      app_commands.Choice(name="Track Log Filters Out Non Ship Entries?",value="logFiltersNonShips"),
      app_commands.Choice(name="Inventory Log Channel",value="inventoryLogChannel"),
      app_commands.Choice(name="Auto-Translate Enabled?",value="translationBool")
    ])
  async def servconfig(self,interaction: discord.Interaction,option: app_commands.Choice[str],input:str):
    #print("Started Serverconfig Slash")
    chk = lists.slashcheckperms(interaction.guild_id,interaction.user.id)
    if chk == True:
      print("Slash Command: Server Config")
      print(f"Guild ID: {interaction.guild_id}; Guild Name: {interaction.guild.name}")
      print(f"User ID: {interaction.user.id}; User Name: {interaction.user.global_name}")
      val = 0
      val=input
      print(option.value)
      if option.value == "distship":
        val=str(input)
      elif option.value=="clanPercent":
        val=float(input)
      elif option in ["verbal","logFiltersNonShips","translationBool"]:
        val=False
        if option.lower() in ["true","yes","on","1","True"]:
          val=True
        elif option.lower() in ["false","no","off","0","False"]:
          val=False
        else:
          return await ctx.send(f"Sorry, {option} is not a valid input. Please use `True` or `False`.")
      elif option.value == "storebal":
        val=str(input.lower())
      else:
        val=int(input)
      data=lists.readFile("config")
      data[str(interaction.guild_id)][str(option.value)]=val
      lists.setFile("config",data)
      await interaction.response.send_message(f'Changed {option.name} to {val}')
    else:
      await interaction.response.send_message("You are not authorized to manage server configuration settings.")

  @commands.command(name="serverconfigalt",description="Server Config Command (LR)",help="Server Config Command, Use n!confighelp for a list of what the values mean.\nOptions: https://github.com/JaWarrior12/New-Light/wiki/Setup-Guide#config-settings")
  async def serverconfigalt(self,ctx,option,*,input):
      chk = lists.checkperms(ctx)
      if chk == True:
        val = 0
        val=input
        if option == "distship":
          val=str(input)
        elif option=="clanPercent":
          val=float(input)
        elif option in ["verbal","logFiltersNonShips","translationBool"]:
          val=False
          if option.lower() in ["true","yes","on","1","True"]:
            val=True
          elif option.lower() in ["false","no","off","0","False"]:
            val=False
          else:
            return await ctx.send(f"Sorry, {option} is not a valid input. Please use `True` or `False`.")
      elif option.value == "storebal":
          val=str(input.lower())
        else:
          val=int(input)
        opt=option
        print(opt)          
        data=lists.readFile("config")
        data[str(ctx.message.guild.id)][opt]=val
        lists.setFile("config",data)
        await ctx.send(f'Changed {(option)} to {val}')

  @commands.command(name='serversettings',brief="Lists Server Settings.",help="Lists The Configuration Settings Of The Server")
  async def listserversettings(self,ctx):
    if str(ctx.message.author.id) not in banned:
      data = None
      chk = lists.checkperms(ctx)
      gid = str(ctx.message.guild.id)
      if chk == True:
        data = lists.readFile("config")
        try:
          e = discord.Embed(title="Configuration Settings For "+ctx.message.guild.name)
          e.add_field(name="Verify Logs?",value=data[gid]["verbal"],inline=True)
          e.add_field(name="Store Member Balances?",value=data[gid]["storebal"],inline=True)
          e.add_field(name="Require Proof When Not Using Distro Log Verification?",value=data[gid]["nonverProof"],inline=True)
          e.add_field(name="Clan Percent",value=data[gid]["clanPercent"],inline=True)
          e.add_field(name="Clan Storage Hex Code",value=data[gid]["distship"],inline=True)
          e.add_field(name="Distribution Logging  Channel",value=ctx.guild.get_channel(data[gid]["distchan"]).mention,inline=True)
          e.add_field(name="Ping Channel",value=ctx.guild.get_channel(data[gid]["pingchan"]).mention,inline=True)
          e.add_field(name="Member Channel",value=ctx.guild.get_channel(data[gid]["memchan"]).mention,inline=True)
          e.add_field(name="Member Role",value=ctx.guild.get_role(data[gid]["memrole"]).mention,inline=True)
          e.add_field(name="Member List Message",value=ctx.guild.get_channel(data[gid]["memchan"]).get_partial_message(data[gid]["memmsg"]).jump_url,inline=True)
          e.add_field(name="Track Log Channel",value=ctx.guild.get_channel(data[gid]["trackLogChannel"]).mention,inline=True)
          e.add_field(name="Track Log Filters Non Ship Entries?",value=ctx.guild.get_channel(data[gid]["logFiltersNonShips"]),inline=True)
          e.add_field(name="Inventory Log Channel",value=ctx.guild.get_channel(data[gid]["inventoryLogChannel"]),inline=True)
          e.add_field(name="Auto-Translation Active?",value=ctx.guild.get_channel(data[gid]["translationBool"]),inline=True)
          await ctx.send(embed=e)
        except KeyError:
          await ctx.send(f"KeyError: Guild {gid} cannot be found.")
      else:
        await ctx.send("You are not leadership Authorized")
    elif str(ctx.message.author.id) in banned:
      await ctx.send("Your ID Is In The Banned List.")
    else:
      await ctx.send("Error")

  @commands.command(name="memberlistconfig",aliases=["mlc"],brief="Setup member list.",help="Setup member list, n!mlc (LR)",hidden=False,disabled=False)
  async def mlc(self,ctx):
    FILTERED_ROLES=["admin"]
    if lists.checkperms(ctx)==True:
      if lists.readFile("config")[str(ctx.message.guild.id)]["memchan"]==0:
        await ctx.send("Member List Channel Not Configured, Please Use /serverconfig to desigante your member channel.")
      if lists.readFile("config")[str(ctx.message.guild.id)]["memrole"]==0:
        await ctx.send("Member Role Not Configured, Please use /serverconfig to designate your member role.")
      else:
        gid=str(ctx.message.guild.id)
        await self.updatememlist(self,gid)
        await ctx.send(f"Member List Created")
    else:
      await ctx.send("Not authorized to use leadership commands in this server")

  @tasks.loop(hours=6)
  async def runUpdateMemList(self):
    await self.updatememlist(self,"all")

  @commands.command(name="devRunUpdateMemList",aliases=["devRUML"],help="Forces a memberlist update without creating a new message")
  async def devRunUpdateMemList(self,ctx,servers="dev"):
    if ctx.author.id in developers:
      await ctx.send("Starting MemList Update")
      await self.updatememlist(self,servers)
      await ctx.send("MemList Update Complete")

  @staticmethod
  async def updatememlist(self,servers):
    serversList=[]
    if servers=="dev":
      serversList=[self.bot.get_guild(1031900634741473280)]
    elif servers=="DNU":
      pass
    elif servers=="all":
      serversList=[guild for guild in self.bot.guilds]
    else:
      splitList=servers.split(",")
      serversList=[self.bot.get_guild(int(gldid)) for gldid in splitList]
    for g in serversList:
      try:
        cuts=[]
        ctnt3=""
        data=lists.readFile("config")
        if str(g.id) in list(data.keys()):
          pass
        else:
          continue
        if lists.readFile("config")[str(g.id)]["memchan"]==0:
          pass
        elif lists.readFile("config")[str(g.id)]["memrole"]==0:
          pass
        else:
          gid=str(g.id)
          guild=self.bot.get_guild(g.id)
          data=lists.readFile("config")
          memchan=lists.readFile("config")[str(guild.id)]["memchan"]
          channel=await guild.fetch_channel(int(memchan))
          groles=guild.roles
          lists.setFile("config",data)
          memrole=guild.get_role(int(data[gid]["memrole"]))
          ranks=[]
          rnkord=[]
          for x in guild.members:
            roles=x.roles
            lstrle=roles[-1]
            inx=0
            for role in roles:
              if role.id==memrole.id:
                inx=roles.index(role)+1
                rid=roles[-1].id
                roleb=guild.get_role(rid)
                if roleb.name=="@everyone":
                  pass
                elif roleb.name in FILTERED_ROLES or any(i in roleb.name for i in CONTAINS_ROLE_FILTER):
                  roleIndex=-2
                  def getNextRole(roleIndex):
                    rid2=roles[roleIndex].id
                    rolec=guild.get_role(rid2)
                    if rolec.name in FILTERED_ROLES or any(i in rolec.name for i in CONTAINS_ROLE_FILTER):
                      getNextRole(roleIndex-1)
                    else:
                      global roleb
                      roleb=guild.get_role(rid2)
                      if groles.index(roleb) in rnkord:
                        pass
                      else:
                        rnkord.append(groles.index(roleb))
                  getNextRole(roleIndex)
                else:
                  if groles.index(roleb) in rnkord:
                    pass
                  else:
                    rnkord.append(groles.index(roleb))
          gidranks=guild.roles
          rnkord.sort(reverse=True)
          checkedMems=[]
          for x in rnkord:
            rle=gidranks[x].id
            pos=rnkord.index(x)
            ranks.insert(pos,rle)
            rmlist=[]
            mems=list(guild.members)
            for r in ranks:
              rmlistb=[]
              for mem in mems:
                rolesb=mem.roles
                for roleb in rolesb:
                  if roleb.id==r and mem.id not in checkedMems:
                    rmlistb.append(mem.id)
                    checkedMems.append(mem.id)
                  else:
                    pass
              rmlist.append(rmlistb)
            ctnt=""
            for x in ranks:
              rmlistIndex=ranks.index(x)
              def tempStop():
                rle=guild.get_role(x)
                if rle.id==memrole.id:
                  pass
                elif any([x.mention in ctnt for x in rle.members]):
                  pass
                elif len(rle.members)>=1:
                  ctnt=ctnt+"\n\n∙"+rle.mention+" ("+str(len(rle.members))+") :"
                else:
                  pass
                for us in mems:
                  if rle in us.roles and ctnt.find(us.mention)==-1 and memrole in us.roles:
                    ctnt=ctnt+"\n--"+us.mention
                    mems.remove(us)
                  else:
                    pass
              async def tempNew(x):
                ctnt2=""
                rle=guild.get_role(x)
                if rle.id==memrole.id:
                  pass
                elif any([x.mention in ctnt2 for x in rle.members]):
                  pass
                elif len(rle.members)>=1:
                  ctnt2=ctnt2+"\n\n∙"+rle.mention+" ("+str(len(rle.members))+") :"
                else:
                  pass
                for mem in rle.members:
                    us=await guild.fetch_member(mem.id)
                    if rle in us.roles and ctnt2.find(us.mention)==-1 and memrole in us.roles:
                      ctnt2=ctnt2+"\n--"+us.mention
                    else:
                      pass
                return ctnt2
              nextBit=await tempNew(x)
              if int(len(ctnt) + len(nextBit)) < 1930:
                ctnt = ctnt + nextBit
              else:
                if ctnt not in cuts:
                  cuts.append(ctnt)
                ctnt=nextBit
          nextItem=ctnt
          ctnt3Len=len(ctnt3)
          nextItemLen=len(nextItem)
          if int(ctnt3Len+nextItemLen) < 1930:
            ctnt3+=nextItem
          else:
            if ctnt3 not in cuts:
              cuts.append(ctnt3)
            ctnt3=""
        if ctnt3 not in cuts:
          cuts.append(ctnt3)
        try:
         #await channel.purge()
          amount=100
          await channel.purge(limit=amount, check=lambda message: message.author == self.bot.user, reason="Member List Update")
        except:
          pass
        for cut in cuts:
          if len(cut)>0:
            mesg=await channel.send("temp")
            await mesg.edit(content=cut)
        await channel.send(f"\n Total Member Count: `{len(memrole.members)}` \nMember List Updated: `{datetime.datetime.now()}`")
      except Exception as e:
        continue

async def setup(bot: commands.Bot):
  await bot.add_cog(SetupCmds(bot))
