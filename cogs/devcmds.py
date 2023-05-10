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

class DevCmds(commands.Cog, name="Developer Commands",description="Developer Commands + Setupserver command"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.backupdaily.start()
    #self.my_console=Console(bot)
  def cog_unload(self):
    #print(1)
    self.backupdaily.cancel()

  @commands.command(name='ping',brief="Latency Command",help="Latency Command")
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def ping(self,ctx):
    await ctx.send(f"Pong 🏓! Latency: {round(int(self.bot.latency)*1000)}ms")

  @commands.command(name='shutdown',brief="Shuts down and restarts New Light", help="Shuts Down and Restarts New Light. Args: None")
  async def shutdown(self,ctx,msg=None):
    if ctx.message.author.id in developers:
      lists.logback(ctx,msg)
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
      await ctx.send('ONLY DEVELOPERS ARE ALLOWED TO SHUTDOWN THE BOT!!! YOU ARE NOT A DEVELOPER') 

  @commands.command(name='backup', brief="Backs up New Light to the reseve databases", help="Backs up New Light's Databases. Args: None")
  async def backups(self,ctx,*,msg=None):
    if ctx.message.author.id in developers:
      lists.logback(ctx,msg)
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
  
  @commands.command(name='lockdown', brief="Locks down a channel, preventing guests from chatting", help="Licks down a channel and prevents guests from chatting. Args: None", hidden=True)
#@commands.has_permissions(manage_channels = True)
  async def lockdown(self,ctx,*,msg=None):
    lists.logback(ctx,msg)
    if ctx.message.author.id in developers:
      await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
      await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")
    else:
      await ctx.send(f'<@{ctx.message.author.id}> You Are NOT A Developer And CANNOT Lockdown Channels')

  @commands.command(name='unlock', brief='Unlocks A Channel', help="Unlocks a channel. Args: None", hidden=True)
#@commands.has_permissions(manage_channels=True)
  async def unlock(self,ctx):
    if ctx.message.author.id in developers:
      await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
      await ctx.send(ctx.channel.mention + " ***has been unlocked.***")
    else:
      await ctx.send(f'<@{ctx.message.author.id}> You Are NOT A Developer And CANNOT Unlock Channels')
      
  @commands.command(name='addrole',pass_context=True, brief='Addrole Cmd, Broken RN', help="Adds a role to a member. Args: <@Role> <@Member>", hidden=True)
  async def addrole(self,ctx, role: discord.Role, member: discord.Member=None):
    if ctx.message.author.id in developers:
      member = member or ctx.message.author
      print(member)
      print(role)
      await member.add_roles(role)
    else:
      ctx.send("Not A Dev")

  @commands.Cog.listener()
  async def on_member_update(self,before, after):
      if len(before.roles) < len(after.roles):
          newRole = next(role for role in after.roles if role not in before.roles)
  
          if newRole.name == "OfficialMember": #OfficialMember
            gid = before.guild.id
            #lists.updatemsg(gid)
            print("MemList Updated")
          else:
            print("Not OfficialMember Role")

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
    lists.logback(ctx,cog)
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
    lists.logback(ctx,cog)
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
    lists.logback(ctx,cog)
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
    lists.logback(ctx,msg)
    if ctx.message.author.id in developers:
      base_string = "```css\n"  # Gives some styling to the list (on pc side)
      base_string += "\n".join([str(cog) for cog in self.bot.extensions])
      base_string += "\n```"
      await ctx.send(base_string)
    else:
      await ctx.send("Not A Dev")

  @commands.command(name="setupserverold",brief="Setup For Your Server",help="Sets Up Databases and Configs For Your Server. ONLY RUN THIS ONCE!!! Administrator Permissions are required to run this command. It automaticlly adds the person who ran the command to the authorized users list. Ping Channel is for the NL Ping Webpage, simply insert the CHANNEL ID of your Battle Links channel.",hidden=True,disabled=True)
  @commands.has_permissions(administrator=True)
  async def setupsrvrold(self,ctx,pingChannel=None,distroChannel=None):
      servers=lists.readdata()
      if str(ctx.message.guild.id) not in servers.keys():
        msg = None
        lists.logback(ctx,msg)
        msgb = "a b"
        pc=int(pingChannel)
    #if ctx.message.author.id in developers:
      # check if all elements in ls are integers
      #if all([isinstance(item, int) for item in authUs]) == True:
        gid = ctx.message.guild.id
        uid = ctx.message.author.id
        #await lists.logmajor(self,ctx,msg=str(uid))
        default = {}
        defaultb=[]
        defaultc={"auth":[],"pingchan":pc,"distchan":int(distroChannel),"name":ctx.message.guild.name}
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

        #await server.create_role(name="OfficialMember")
        #datac = dumps(lists.readdataE())
      #else:
        #await ctx.send("The AuthorizedUsers list can only be User Id's, only integers are allowed in the list.")
    #else:
      #await ctx.send("You are not a Developer and Can Not run this command.")

  @commands.command(name="adminrole",hidden=True)
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

  @commands.command(name="banb",hidden=True,disabled=True)
  @commands.has_role('Developer')
  async def banuser(self,ctx,user):
    if ctx.message.author.id in developers:
      keya = "all"
      keyb = "ban"
      gid = str(ctx.message.guild.id)
      #mylist = []
      #datab = dumps(lists.readdataE()[keyb]).replace("[","").replace("]","")
      data = dumps(lists.readdataE()[keyb])#.replace("[","").replace("]","").replace(' ',"").replace("'","").replace('"',"")
      if str(user) in banned:
        await ctx.send(f'The User With An Id Of {user} Is Already In The Ban List')
      else:
        #await lists.logmajor(self,ctx,user)
        print(data)
        #await ctx.send(type(data))
        ##await ctx.send(data)
        #await ctx.send("----")
        data=data.replace("[","").replace("]","").replace('"','')
        #await ctx.send(data)
        #await ctx.send(data.split(","))
        mylist = data#.split(",")#.split(",") #[data.replace("'","").replace('"','')]
        #await ctx.send(type(mylist))
        #await ctx.send(mylist)
        if "[]" in mylist:
          mylist.remove("[]")
        #await ctx.send("----")
        #await ctx.send(mylist)
        #await ctx.send("----")
        usr = str(user).replace("'","").replace('"','')
        use = [mylist+","+usr]
        #await ctx.send(use)
        #mylist.append(use)#.replace("'","").replace('"',''))
        #await ctx.send(mylist)
        datab=lists.readdataE()
        datab[keyb]=use
        lists.setdataE(datab)
        await ctx.send(f'The User With A User Id Of {user} has been BANNED from using New Light')
        lists.bannedlist()
    else:
      await ctx.send("You are not a developer and cannot use this command")

  #@commands.Cog.listener()
  #async def on_message(self,msg):
   # print(msg.content)
    #mes = msg.content
    #if "https://" in mes:
      #await msg.delete()

  @commands.command(name='sync', description='Owner only')
  async def sync(self,ctx):
    if ctx.message.author.id in developers:
        await self.bot.tree.sync()
        print('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

  @commands.command(name='joindate', description='Checks Join Date Of New Light', hidden=True)
  async def joindata(self,ctx):
    if ctx.message.author.id in developers:
      me=ctx.message.guild.get_member(974045822167679087)
      date=me.joined_at
      converteddate=date.astimezone(pytz.timezone('US/Eastern'))
      await ctx.message.author.send(f'I joined {ctx.message.guild.name} at {converteddate} (EST).')
    else:
      await ctx.send('You must be the owner to use this command!')

  @tasks.loop(time=times)
  async def backupdaily(self):
    backup(self)

async def setup(bot: commands.Bot):
  await bot.add_cog(DevCmds(bot))