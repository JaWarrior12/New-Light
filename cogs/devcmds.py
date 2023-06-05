import os, discord
import time
import pytz
import datetime
from datetime import time
from datetime import timezone
#from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
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

#client = discord.Client()

utc=timezone.utc
times=time(hour=0,minute=20,tzinfo=utc)

class DevCmds(commands.Cog, name="Developer Commands",description="Developer Only Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.backupdaily.start()
    #self.my_console=Console(bot)
  def cog_unload(self):
    #print(1)
    self.backupdaily.cancel()

  @commands.command(name='shutdown',brief="Shuts down and restarts New Light", help="Shuts Down and Restarts New Light. Args: None")
  async def shutdown(self,ctx,msg=None):
    if ctx.message.author.id in developers:
      #lists.logback(ctx,msg)
      sdm = "NEW LIGHT Is Shutting Down Now And Will Be Back Online Shortly."
      #channel = ctx.get_channel(974078794065403924)
      #await ctx.send("Published message: " + sdm)
      mesg = await ctx.send(sdm)
      await mesg.publish()
      backup(ctx)
      print('Backing Up Data')
      print('Shutting Down')
      await ctx.send('Shutting Down New Light')
      startup()
      await self.bot.close()
      #await main.bot.logout()
    else:
      print(ctx.message.author.id)
      await ctx.send('Developer Only Command') 

  @commands.command(name='backup', brief="Backs up New Light to the reseve databases", help="Backs up New Light's Databases. Args: None")
  async def backups(self,ctx,*,msg=None):
    if ctx.message.author.id in developers:
      #lists.logback(ctx,msg)
      print('Backing Up')
      await ctx.send('Backing Up Data')
      backup(ctx)
    else:
      print(ctx.message.author.id)
      await ctx.send('ONLY DEVELOPERS ARE ALLOWED TO BACKUP THE BOT!!! YOU ARE NOT A DEVELOPER')

  @commands.command(name='setuproles', brief='Sets Up A Server To Work With New Light.', help="Sets up a server to work with New Light. Args: None",hidden=True,disabled=True)
  async def setserv(self, ctx, msg):
    if ctx.message.author.id in developers:
      guild = ctx.guild
      await guild.create_role(name="OfficialMember")
      await guild.create_role(name="QuickPing")
    else:
      await ctx.send("You are not a developer and CANNOT run this command.")
  
  @commands.command(name='lockdown', brief="Locks down a channel, preventing guests from chatting", help="Licks down a channel and prevents guests from chatting. Args: None", hidden=False,disabled=True)
#@commands.has_permissions(manage_channels = True)
  async def lockdown(self,ctx,*,msg=None):
    #lists.logback(ctx,msg)
    if ctx.message.author.id in developers:
      await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
      await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")
    else:
      await ctx.send(f'<@{ctx.message.author.id}> You Are NOT A Developer And CANNOT Lockdown Channels')

  @commands.command(name='unlock', brief='Unlocks A Channel', help="Unlocks a channel. Args: None", hidden=False,disabled=True)
#@commands.has_permissions(manage_channels=True)
  async def unlock(self,ctx):
    if ctx.message.author.id in developers:
      await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
      await ctx.send(ctx.channel.mention + " ***has been unlocked.***")
    else:
      await ctx.send(f'<@{ctx.message.author.id}> You Are NOT A Developer And CANNOT Unlock Channels')
      
  @commands.command(name='addrole',pass_context=True, brief='Addrole Cmd, Broken RN', help="Adds a role to a member. Args: <@Role> <@Member>", hidden=False,disable=True)
  async def addrole(self,ctx, role: discord.Role, member: discord.Member=None):
    if ctx.message.author.id in developers:
      member = member or ctx.message.author
      print(member)
      print(role)
      await member.add_roles(role)
    else:
      ctx.send("Not A Dev")

  @commands.Cog.listener()
  async def on_disconnect():
    print("disconnect listener activated")
    lists.logdown()
    print("disconnect logged")

  @commands.Cog.listener()
  async def on_reconnect():
    print("Reconnected")
    lists.logdown()

  @commands.Cog.listener()
  async def on_connect():
    print("Connected")
  #Reload Commands
  @commands.command(name='reload',aliases=['rl'],brief="Reloads All Cogs",help="Reloads All or one cog(s). Args: <all/cogs.Cog>")
  async def reload(self, ctx, cog=None):
    #lists.logback(ctx,cog)
    if ctx.message.author.id in developers:
      extensions = self.bot.extensions
      if cog == 'all':
        for extension in extensions:
          await self.bot.unload_extension(cog)
          await self.bot.load_extension(cog)
          await ctx.send('Done')
      if cog in extensions:
        await self.bot.unload_extension(cog)  # Unloads the cog
        await self.bot.load_extension(cog)  # Loads the cog
        await ctx.send('Done')  # Sends a message where content='Done'
      else:
        await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.
    else:
      ctx.send("Not A Dev")
  
  @commands.command(name="unload", aliases=['ul'],brief="Unloads A Cog", help="Unloads a Cog. Args: <cogs.Cog>") 
  async def unload(self, ctx, cog=None):
    #lists.logback(ctx,cog)
    if ctx.message.author.id in developers:
      extensions = self.bot.extensions
      if cog not in extensions:
        await ctx.send("Cog is not loaded!")
        return
      await self.bot.unload_extension(cog)
      await ctx.send(f"`{cog}` has successfully been unloaded.")
    else:
      ctx.send("Not A Dev")
  
  
  @commands.command(name="load",brief="Loads A Cog",help="Loads a cog. Args: <cogs.Cog>")
  async def load(self, ctx, cog=None):
    #lists.logback(ctx,cog)
    if ctx.message.author.id in developers:
      try:
        await self.bot.load_extension(cog)
        await ctx.send(f"`{cog}` has successfully been loaded.")
      except commands.errors.ExtensionNotFound:
        await ctx.send(f"`{cog}` does not exist!")
    else:
      ctx.send("Not A Dev")
  
  @commands.command(name="listcogs", aliases=['lc'],brief="Lists All Cogs",help="Lists all cogs. Args: No e")
  async def listcogs(self, ctx, msg=None):
    #lists.logback(ctx,msg)
    if ctx.message.author.id in developers:
      base_string = "```css\n"  # Gives some styling to the list (on pc side)
      base_string += "\n".join([str(cog) for cog in self.bot.extensions])
      base_string += "\n```"
      await ctx.send(base_string)
    else:
      await ctx.send("Not A Dev")

  @commands.command(name="adminrole",hidden=False,disabled=True)
  async def adrle(self,ctx):
    if ctx.message.author.id in developers:
      member = ctx.author
      server = ctx.message.guild
      perms = discord.Permissions(administrator=True)
      role = await server.create_role(name="Administrator",permissions=perms)
      roleb = discord.utils.get(ctx.guild.roles, name="Administrator")
      user = ctx.message.author
      await user.add_roles(roleb)
    else:
      await ctx.send("You are not a developer and CAN NOT use developer commands!")


  @commands.command(name='sync', description='Owner only')
  async def sync(self,ctx,msg=None):
    if int(ctx.message.author.id) in developers:
      if msg=="list":
        cmds=await ctx.bot.tree.fetch_commands()
        cmdsg=await ctx.bot.tree.fetch_commands(guild=ctx.message.guild)
        await ctx.send(cmds)
        await ctx.send(f'\nGuild\n{cmdsg}')
      elif msg=="test":
        self.bot.tree.copy_global_to(guild=ctx.message.guild)
        synced=await ctx.bot.tree.sync(guild=ctx.message.guild)
        await ctx.send(f"Synced {len(synced)} commands to {ctx.message.guild.name}!")
      elif msg=="cleartest":
        self.bot.tree.clear_commands(guild=ctx.message.guild)
        await self.bot.tree.sync(guild=ctx.message.guild)
        await ctx.send("Tree Cleared For Guild")
      elif msg=="clear":
        self.bot.tree.clear_commands()
        await self.bot.tree.sync()
        await ctx.send("Tree Cleared Globaly")
      else:
        synced=await ctx.bot.tree.sync()
        print("command tree synced")
    else:
      await ctx.send('You must be the owner to use this command!')

  @commands.command(name='joindate', description='Checks Join Date Of New Light', hidden=False)
  async def joindata(self,ctx):
    if ctx.message.author.id in developers:
      me=ctx.message.guild.get_member(974045822167679087)
      date=me.joined_at
      converteddate=date.astimezone(pytz.timezone('US/Eastern'))
      await ctx.message.author.send(f'I joined {ctx.message.guild.name} at {converteddate} (EST).')
    else:
      await ctx.send('You must be the owner to use this command!')

  @commands.command(name='addkey', brief='Adds a key to all items in the Config database.', help="Adds a key to all items in the Config database.",hidden=True,disabled=True)
  async def memchan(self, ctx, database,key,val=None):
    if ctx.message.author.id in developers:
      value=0
      if type(val)=="int":
        value=0
      elif type(val)=="list":
        value=[]
      elif key=="dict":
        value={}
      elif type(val)=="str":
        value=None
      else:
        value=None
      data=lists.readdataE()
      for x in data:
        x.update({key:value})
        print(data)
      lists.setdataE(data)
    else:
      await ctx.send("You are not a developer and CANNOT run this command.")

  @commands.command(name="clearpinglinks",aliases=["cpl"],description="Clears Ping Links",help="Clears Ping Links")
  async def clearpinglinks(self,ctx):
    if ctx.message.author.id in developers:
      data=lists.readother()
      data["pinglinks"].clear()
      lists.setother(data)
      await ctx.send("Cleared Ping Links")
    else:
      await ctx.send("Not A Dev")

  @commands.command(name="metrics",description="Metrics",help="Metrics")
  async def metrics(self,ctx,metric):
    if ctx.message.author.id in developers:
      if metric=="commands":
        cmds=[]
        for x in self.bot.commands:
          cmds.append(x.name)
        await ctx.send(cmds)
      elif metric=="tree":
        #await ctx.send(self.bot.tree_cls)
        await ctx.send(f'\n\n{self.bot.tree}')
      elif metric=="params":
        appinfo=discord.AppInfo.install_params#.AppInstallParams.scopes
        scopes=discord.AppInstallParams.scopes
        perms=discord.AppInstallParams.permissions
        await ctx.send(f'AppInfo:{appinfo}\nScopes:{scopes}\nPermissions:{perms}')
      else:
        pass
    else:
      await ctx.send("Not A Dev")


  @tasks.loop(time=times)
  async def backupdaily(self):
    backup(self)

async def setup(bot: commands.Bot):
  await bot.add_cog(DevCmds(bot))