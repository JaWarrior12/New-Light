import os, discord
import time
import pytz
import datetime
#from keep_alive import keep_alive
from discord.ext import commands, tasks
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
    self.updatememlist.start()
    #self.my_console=Console(bot)
  def cog_unload(self):
    #print(1)
    self.updatememlist.cancel()

  def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id or ctx.author.id in lists.developers
    return commands.check(predicate)

  @commands.command(name="setupserver",brief="Setup For Your Server (Servr Owner Only)",help="Sets Up Databases and Configs For Your Server. ONLY RUN THIS ONCE!!! Administrator Permissions are required to run this command. It automaticlly adds the person who ran the command to the authorized users list. Ping Channel is for the NL Ping Webpage, simply insert the CHANNEL ID of your Battle Links channel.\ndistroChannel is the ID of your distribution channel.\nclanPercent is the percent of flux from each distro log that goes to the clan. Must be the server owner to run this, if the server owner is unavailable you can contact jawarrior about completing server setup.")
  #@commands.has_permissions(administrator=True)
  @commands.check_any(is_guild_owner())
  async def setupsrvr(self,ctx,pingChannel=0,distroChannel=0,clanPercent=0,distShip=None,memRole=0,storebals="no",memchan=0,verbal="no"):
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
        defaultc={"auth":[str(uid)],"pingchan":pc,"distchan":int(distroChannel),"clanPercent":float(clanPercent),"distship":str(distShip),"memrole":memRole,"storebal":storebals,"name":str(ctx.message.guild.name),"memchan":memchan,"memmsg":0,"verbal":verbal}
        defaultd={"clan":{"flux":0,"iron":0,"explosive":0,"rc":0,"burst":0,"auto":0,"loader":0,"pusher":0,"rubber":0,"handheld":0,"ice":0,"item_launcher":0,"rcd":0}}
        data = lists.readdata()
        data[gid]=dict(defaultd)
        lists.setdata(data)
        data = lists.readdataB()
        data[gid]=defaultb
        lists.setdataB(data)
        data = lists.readdataC()
        data[gid]=default
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
        await ctx.send("Server Setup Succesfully!")
        await server.create_role(name="QuickPing")
        await ctx.send("QuickPing Role Created")
      else:
        await ctx.send("Server already setup.")

  @commands.command(name="authuser",breif="Authorizes User For LR Commands (LR)",help="Authorizes A User To Use Leadership Commands. Required Permissions: Administrator; Format: n!authuser <USERID>")
  #@commands.has_permissions(administrator=True)
  @commands.check_any(is_guild_owner())
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

  
  @commands.command(name="deauthuser",brief="Removes a user's LR access. (LR)",help="Removes Authorization From A User To Use Leadership Commands. Required Permissions: Administrator; Format: n!deauthuser <USERID>")
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

  @commands.command(name="authlist",brief="Gets Servers LR Authorized List (Server Owner Only)",help="Lists all users authorized to use leadership commands in the server.")
  @commands.check_any(is_guild_owner())
  async def authlist(self,ctx):
    if str(ctx.message.author.id) not in banned:
      msg="none"
      msgb = str(msg)
      chk = lists.checkperms(ctx)
      gid = str(ctx.message.guild.id)
      #lists.logback(ctx,msgb)
      list=lists.readdataE()
      if chk == True:
        for mem in list[str(ctx.message.guild.id)]["auth"]:
          member=ctx.message.guild.get_member(int(mem))
          await ctx.send(f'Name:{member.display_name}; ID:{member.id}')
    else:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')

  @commands.command(name="confighelp",help="Description of ServerConfig Settings")
  async def conhelp(self,ctx):
    await ctx.send("Server Settings\n-Ping Channel (pingchan)==Channel ID Of Server's Battle Links Channel\n-Distribution Channel (distchan)==Channel ID Of Server's Distro Logging Channel\n-Clan Percent (clanPercent)==What Percent Of Items In Logs Go To The Clan\n-Clan Storage (distship)==HexCode Of Clan Storage\n-Member Role (memrole)==ID Of Member Role\n-Store Member Balances? (membal)==Will You Store Member Balances In CLAN STORAGE Or Distribute Right After Missions? (Yes/No)\nMember List Channel (memchan)== Member List Channel\nVerify Distribution Logs? (verbal)==Controls What Setting The Automated Distribution Logger Runs (Yes/No)")

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
      app_commands.Choice(name="Verify Distribution Logs?",value="verbal")
    ])
  async def servconfig(self,interaction: discord.Interaction,option: app_commands.Choice[str],input:str):
    #print("Started Serverconfig Slash")
    chk = lists.slashcheckperms(interaction.guild_id,interaction.user.id)
    if chk == True:
      val = 0
      val=input
      print(option.value)
      if option.value == "distship":
        val=str(input)
      elif option.value=="clanPercent":
        val=float(input)
      elif option.value == "storebal" or option.vale=="verbal":
        val=str(input.lower())
      else:
        val=int(input)
      data=lists.readdataE()
      data[str(interaction.guild_id)][str(option.value)]=val
      #print(data)
      lists.setdataE(data)
      await interaction.response.send_message(f'Changed {(option.name)} to {val}')
    else:
      await interaction.response.send_message("You are not authorized to manage server configuration settings.")

  @commands.command(name="serverconfigalt",description="Server Config Command (LR)",help="Server Config Command, Use n!confighelp for a list of what the values mean.\nOptions: distship;\n-clanPercent;\n-storebal;\n-distchan;\n-pingchan;\n-memrole;\n-memchan")
  async def serverconfigalt(self,ctx,option,*,input):
      chk = lists.checkperms(ctx)
      if chk == True:
        val = 0
        val=input
        if option == "distship":
          val=str(input)
        elif option=="clanPercent":
          val=float(input)
        elif option == "storebal" or option=="verbal":
          val=str(input.lower())
        else:
          val=int(input)
        print(val)
        data=lists.readdataE()
        data[str(ctx.message.guild.id)][str(option.lower)]=val
        print(data)
        #print(data)
        lists.setdataE(data)
        await ctx.send(f'Changed {(option)} to {val}')

  @commands.command(name="memberlistconfig",aliases=["mlc"],brief="Setup member list.",help="Setup member list, n!mlc (LR)",hidden=True,disabled=False)
  async def mlc(self,ctx):
    if lists.checkperms(ctx)==True:
      if lists.readdataE()[str(ctx.message.guild.id)]["memchan"]==0:
        await ctx.send("Member List Channel Not Configured, Please Use /serverconfig to desigante your member channel.")
      if lists.readdataE()[str(ctx.message.guild.id)]["memrole"]==0:
        await ctx.send("Member Role Not Configured, Please use /serverconfig to designate your member role.")
      else:
        gid=str(ctx.message.guild.id)
        #lists.logback(ctx,msg=None)
        memchan=lists.readdataE()[str(ctx.message.guild.id)]["memchan"]
        channel=await ctx.message.guild.fetch_channel(int(memchan))
        nmesg=await channel.send("Member List Message")
        groles=ctx.message.guild.roles
        #message=await channel.fetch_message(nmesg)
        #print(nmesg.id)
        data=lists.readdataE()
        data[str(ctx.message.guild.id)]["memmsg"]=int(nmesg.id)
        lists.setdataE(data)
        await ctx.send("Message Configured, Adding Members")
        memrole=ctx.message.guild.get_role(int(data[gid]["memrole"]))
        ranks=[]
        rnkord=[]
        for x in ctx.message.guild.members:
          #print(x.display_name)
          #print(x.roles)
          roles=x.roles
          #print(roles)
          lstrle=roles[-1]
          inx=0
          for role in roles:
            if role.id==memrole.id:
              print(f'Role Pos:{roles.index(role)}')
              inx=roles.index(role)+1
              print(f'Index:{inx}')
              rid=roles[inx].id
              roleb=ctx.message.guild.get_role(rid)
              print(roleb)
              #print(rnk)
              if roleb.name=="@everyone":
                pass
              else:
                if groles.index(roleb) in rnkord:
                  pass
                else:
                  #ranks.append(rnk)
                  rnkord.append(groles.index(roleb))

        #await ctx.send(ranks)
        gidranks=ctx.message.guild.roles
        rnkord.sort(reverse=True)
        print(rnkord)
        for x in rnkord:
          rle=gidranks[x].id
          pos=rnkord.index(x)
          ranks.insert(pos,rle)
        print(rnkord)
        print(ranks)
        print(groles[9])
        rmlist=[]
        mems=list(ctx.message.guild.members)
        #print(mems)
        for r in ranks:
          rmlistb=[]
          for mem in mems:
            #print(mem)
            rolesb=mem.roles
            for roleb in rolesb:
              #print(roleb)
              #print(r)
              if roleb.id==r:
                rmlistb.append(mem.id)
              else:
                pass
          rmlist.append(rmlistb)
        #await ctx.send(rmlist)
        #await ctx.send(ranks)
        ctnt=""
        for x in ranks:
          rle=ctx.message.guild.get_role(x)
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
        await nmesg.edit(content=ctnt)
        await ctx.send(f"Member List Created: {nmesg.jump_url}")
    else:
      await ctx.send("Not authorized to use leadership commands in this server")

  @tasks.loop(hours=1)
  async def updatememlist(self):
    try:
      for g in self.bot.guilds:
        if lists.readdataE()[str(g.id)]["memchan"]==0:
          pass
        elif lists.readdataE()[str(g.id)]["memrole"]==0:
          pass
        else:
          #print("Member Updated")
          gid=str(g.id)
          guild=self.bot.get_guild(g.id)
          #print(guild.name)
          data=lists.readdataE()
          memchan=lists.readdataE()[str(guild.id)]["memchan"]
          channel=await guild.fetch_channel(int(memchan))
          nmesg=await channel.fetch_message(int(data[str(guild.id)]["memmsg"]))
          groles=guild.roles
          #message=await channel.fetch_message(nmesg)
          data[str(guild.id)]["memmsg"]=int(nmesg.id)
          lists.setdataE(data)
          memrole=guild.get_role(int(data[gid]["memrole"]))
          ranks=[]
          rnkord=[]
          for x in guild.members:
            #print(x.display_name)
            #print(x.roles)
            roles=x.roles
            #print(roles)
            lstrle=roles[-1]
            inx=0
            for role in roles:
              if role.id==memrole.id:
                #print(f'Role Pos:{roles.index(role)}')
                inx=roles.index(role)+1
                #print(f'Index:{inx}')
                rid=roles[inx].id
                roleb=guild.get_role(rid)
                #print(roleb)
                #print(rnk)
                if roleb.name=="@everyone":
                  pass
                else:
                  if groles.index(roleb) in rnkord:
                    pass
                  else:
                    #ranks.append(rnk)
                    rnkord.append(groles.index(roleb))
          gidranks=guild.roles
          rnkord.sort(reverse=True)
          #print(rnkord)
          for x in rnkord:
            rle=gidranks[x].id
            pos=rnkord.index(x)
            ranks.insert(pos,rle)
            rmlist=[]
            mems=list(guild.members)
            #print(mems)
            for r in ranks:
              rmlistb=[]
              for mem in mems:
                #print(mem)
                rolesb=mem.roles
                for roleb in rolesb:
                  #print(roleb)
                  #print(r)
                  if roleb.id==r:
                    rmlistb.append(mem.id)
                  else:
                    pass
              rmlist.append(rmlistb)
            #await ctx.send(rmlist)
            #await ctx.send(ranks)
            ctnt=""
            for x in ranks:
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
            await nmesg.edit(content=ctnt)
    except: 
      pass

async def setup(bot: commands.Bot):
  await bot.add_cog(SetupCmds(bot))