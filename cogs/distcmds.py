import os, discord
import time as timea
import asyncio
import pytz
import datetime
from datetime import datetime, timedelta, timezone
from datetime import time as tme
#from apscheduler.schedulers.background import BackgroundScheduler
from threading import Timer
import urllib.request
import requests
import gzip
#from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.utils import get
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup
#from dpyConsole import Console

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

#tz = pytz.timezone('America/New_York')
utc=timezone.utc
tmes=tme(hour=0,minute=20,tzinfo=utc)

class DistCmds(commands.Cog, name="Distribution Commands",description="Loot Distribution Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.verifyscheduled.start()
    #self.my_console=Console(bot)
  def cog_unload(self):
    #print(1)
    self.verifyscheduled.cancel()
    
  #def workaround(self):
    #asyncio.run(self.verifyscheduled())
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    #loop.run_until_complete(self.verifyscheduled())
    #loop.close()

  #async def setup_hook(self) -> None:
    # create the background task and run it in the background
    #self.bg_task = self.loop.create_task(self.verifyscheduled())

  @commands.command(name="logloot",brief="Adds/Subtracts loot from a user's balance. (LR)",help="Adds/Subtracts from a user's balance. The format is: n!logloot @User item amount. If you are subtracting make the amount negative.")
  async def returnpaymentdata(self, ctx, member: discord.Member, item, amount):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        msgb = str(member)+" "+item+" "+amount
        #lists.logback(ctx,msgb)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        if member=="clan":
          pass
        else:
          memvar=member
        try:
          nf = int(dumps(lists.readdata()[gid][str(member.id)][str(item)]).replace(':','=').replace('{','').replace('}','').replace('"',''))
          ns = int(amount)
          added = ns + nf
          if chk == True:
            data[gid][str(member.id)][str(item)] = int(added)
            lists.setdata(data)
            #await ctx.send(f'Now {member.name} has {added} {item} in {ctx.message.guild.name}')
            e = discord.Embed(title="Member Balance Update")
            e.add_field(name="Target Member", value=memvar.display_name, inline=True)
            e.add_field(name="Updated By", value=ctx.message.author.display_name, inline=True)
            e.add_field(name="Old Balance",value=nf,inline=True)
            e.add_field(name="New Balance",value=added,inline=True)
            e.add_field(name="Item",value=item,inline=True)
            e.add_field(name="Amount Added",value=ns,inline=True)
            e.set_thumbnail(url=memvar.display_avatar)
            #tz = pytz.timezone('America/New_York')
            e.timestamp=datetime.now()
            await ctx.send(embed=e)
          else:
            await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")
        except KeyError:
          await ctx.send(f"KeyError: Either Item {item} Or User {member} cannot be found in {ctx.message.guild.name}'s Distribution List.")
          
  @commands.command(name='reset',brief="Resets a member's balance. (LR)",help="Resets one loot value in a user's balance. Format: n!reset @User item")
  async def resetalldata(self, ctx, member: discord.Member, item):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        msgb=str(member)+" "+item
        #lists.logback(ctx,msgb)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        if chk == True:
          try:
            data[gid][str(member.id)][str(item)]=0
            lists.setdata(data)
            memvar=member
            e = discord.Embed(title="Member Balance Reset")
            e.add_field(name="Target Member", value=memvar.display_name, inline=True)
            e.add_field(name="Reset By", value=ctx.message.author.display_name, inline=True)
            e.add_field(name="Item",value=item,inline=True)
            e.set_thumbnail(url=memvar.display_avatar)
            #tz = pytz.timezone('America/New_York')
            e.timestamp=datetime.now()
            await ctx.send(embed=e)
          except KeyError:
            await ctx.send(f"KeyError: Either Item {item} Or User {member} cannot be found in {ctx.message.guild.name}'s Distribution List.")
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")
          
  @commands.command(name='balance',brief="Calls a user's balance.",help="Calls a member's balance. Just ping the user in the command. Format: n!balance @user")
  async def getuserloot(self,ctx,member: discord.Member):
    if str(ctx.message.author.id) not in banned:
      data = None
      print(member.id)
      #chk = lists.checkperms(ctx)
      gid = str(ctx.message.guild.id)
      #lists.logback(ctx,member)
      #if chk == True:
      data = lists.readdata()
      try:
        memvar=member
        e = discord.Embed(title="Member Balance")
        e.add_field(name="Member", value=memvar.display_name, inline=True)
        for x in data[gid][str(member.id)].keys():
          e.add_field(name=x,value=data[gid][str(member.id)][x],inline=True)
        e.set_thumbnail(url=memvar.display_avatar)
        #tz = pytz.timezone('America/New_York')
        e.timestamp=datetime.now()
        await ctx.send(embed=e)
      except KeyError:
        await ctx.send(f"KeyError: User {member} cannot be found in {ctx.message.guild.name}'s Distribution List.")
    elif str(ctx.message.author.id) in banned:
      await ctx.send("Your ID Is In The Banned List.")
    else:
      await ctx.send("Error")

  @commands.command(name="addmember",brief="Adds a member to the clan's distribution database. (LR)", help="Adds a member to the distribution database. Just ping the user in the command. Format: n!addmember @User")
  async def addmember(self,ctx, member: discord.Member):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        #lists.logback(ctx,member)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        if chk == True:
          inputv={}
          keylist=lists.readother()["defaultdist"].keys()
          #await ctx.send(keylist)
          if str(ctx.message.guild.id) in keylist:
            items=lists.readother()["defaultdist"][str(ctx.message.guild.id)]
            for x in items:
              inputv.update({str(x):0})
          else:
            inputv = {"flux":0,"loaders":0,"rcs":0,"pushers":0}
          data[gid][str(member.id)]=dict(inputv)
          lists.setdata(data)
          memvar=member
          e = discord.Embed(title="Member Added")
          e.add_field(name="Member", value=memvar.display_name, inline=True)
          e.add_field(name="Added By",value=ctx.message.author.display_name,inline=True)
          e.add_field(name="Default Balance",value=inputv,inline=True)
          e.set_thumbnail(url=memvar.display_avatar)
          #tz = pytz.timezone('America/New_York')
          e.timestamp=datetime.now()
          await ctx.send(embed=e)
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")

  @commands.command(name="removemember",brief="Removes a member from a clan's distribution database. (LR)", help="Removes a member from the distribution database. Just ping the user in the command and it will remove them. Format: n!removemember @User")
  async def remmem(self,ctx,member: discord.Member,*,reason=None):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        mem=str(member.id)
        del data[gid][mem]
        #lists.logback(ctx,member)
        if chk == True:
          try:
            lists.setdata(data)
            memvar=member
            e = discord.Embed(title="Member Removed")
            e.add_field(name="Member", value=memvar.display_name, inline=True)
            e.add_field(name="Removed By By",value=ctx.message.author.display_name,inline=True)
            e.add_field(name="Reason",value=reason,inline=True)
            e.set_thumbnail(url=memvar.display_avatar)
            #tz = pytz.timezone('America/New_York')
            e.timestamp=datetime.now()
            await ctx.send(embed=e)
          except KeyError:
            await ctx.send(f"KeyError: User {member} cannot be found in {ctx.message.guild.name}'s Distribution List.")
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")

  @commands.command(name='balall',brief="Calls All Clan Balances (LR)",help="Calls all balances in a clan's distribution database. Format: n!balall")
  async def balanceall(self,ctx):
        clan = ctx.message.guild
        #msgparts, data = msg.split(" "), lists.readdata()
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        #lists.logback(ctx,clan)
        mesg = str(gid)
        if chk == True:
          await ctx.send('Balances Of All Members')
          memlist=list(lists.readdata()[mesg].keys())
          cntntlist=[]
          for x in memlist:
            if x == "clan":
              cntntlist.append(f'{x} : {lists.readdata()[mesg][str(x)]}')
            else:
              usid=x
              guild=self.bot.get_guild(int(ctx.message.guild.id))
              uname=guild.get_member(int(usid))
              usbal=lists.readdata()[mesg][str(x)]
              cntntlist.append(f'{uname.name} : {usbal};')
            a=0
          for i in cntntlist:
            await ctx.send(i)
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")

  @commands.command(name="defaultbal",brief="Sets a clan's default balance (LR)",help="Sets the default balance, enter each item separated by a semi-colon (;). Ex. flux;rubber;loaders;rcs",description="Hi")
  async def defaultbal(self,ctx,*,items):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      #lists.logback(ctx,items)
      if chk == True:
        list=items.split(";")
        data=lists.readother()
        data["defaultdist"][str(ctx.message.guild.id)]=list
        lists.setother(data)
        e = discord.Embed(title="Default Balance Updated")
        e.add_field(name="Updated By",value=ctx.message.author.display_name,inline=True)
        e.add_field(name="Default Balance",value=list,inline=True)
        e.set_thumbnail(url=ctx.message.author.display_avatar)
        #tz = pytz.timezone('America/New_York')
        e.timestamp=datetime.now()
        await ctx.send(embed=e)
      else:
        await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")
    else:
      await ctx.send("Your ID Is In The Banned List.")

  #def workaround():
    #asyncio.run(verifyschedule("a"))

  async def restarttimer(self):
    x=datetime.today()
    tz = pytz.timezone('America/New_York')
    x=datetime.today()
    y = x.replace(day=x.day, hour=0, minute=5, second=0, microsecond=0) + timedelta(days=1)
    delta_t=y-x
    secs=delta_t.total_seconds()
    #client=commands.Bot
    #t = Timer(secs, self.workaround)
    #t.start()
    print("Restarted Timer")
    
  @tasks.loop(minutes=5)#time=tmes)
  async def verifyscheduled(self):
    print("Verifying Distro Logs")
    a=0
    data=lists.readdataE()
    oth=lists.readother()
    distdat=lists.readdata()
    for x in oth["verifydist"]:
      loc = oth["verifydist"].index(x)
      gid=x[0]
      chanid=int(x[1])
      msgid=x[2]
      prebal=x[3]
      endbal=x[4]
      ctxt=x[5]
      count=x[7]
      purp=x[8]
      guild=self.bot.get_guild(int(gid))
      channel=guild.get_channel(chanid)
      mesg=await channel.fetch_message(int(msgid))
      try:
        if str(mesg.guild.id) in list(data.keys()):
          distro=int(data[str(mesg.guild.id)]["distchan"])
          if int(mesg.channel.id)==distro:
            pts=ctxt.split("\n")
            pts=list(pts)
            date=pts[4].split("/")
            hex=str("{"+str(pts[3])+"}")
            ds=data[str(mesg.guild.id)]["distship"]
            distship=str("{"+ds+"}")
            distshipb=ds
            if purp.lower()=="withdrawal":
              temp=hex
              hex=distship
              distship=temp
            strgnew=lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{date[2]}_{date[0]}_{date[1]}/ships.json.gz')
            jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{date[2]}_{date[0]}_{date[1]}/log.json.gz')
            def find_routea(data, route_no):
              return list(filter(lambda x: x.get("src") == route_no, data))
            route = find_routea(jsondata,hex)
            remain=list(filter(lambda x: x.get("dst") == distship, route))
            result=0
            ct=0
            cd={}
            for f in remain:
              hexa=hex
              distshipa=distship
              if f['dst']==distshipa and f['src']==hexa:
                cbal=list(filter(lambda f: f.get('hex_code') == ds, strgnew))
                formbal=lists.formItem(f)
                keys=list(formbal.keys())
                ct=ct+formbal[keys[0]]
                cd.update({keys[0]:ct})
              else:
                pass
            for p in list(cd.keys()):
              if p not in list(count.keys()):
                cd.pop(p)
            cdkys=list(cd.keys())
            if purp.lower()=="withdrawal":
              obj=cd[cdkys[0]]
              cd[cdkys[0]]= -abs(obj)
            if cd == count:
              result=1
            else:
              result=2
            if result==1:
              await mesg.add_reaction("✅")
              distdat[str(mesg.guild.id)]=x[6]
              lists.setdata(distdat)
            else:
              await mesg.add_reaction("❌")
            print("Reaction Added")
          else:
            pass
        else:
          pass
        oth["verifydist"].remove(x)
      except Exception as e:
        if hasattr(e, 'message'):
          emes=e.message
        else:
          emes=e
        print(emes)
        await mesg.add_reaction("🤷")
        print("Error Occured")
    others=lists.readother()
    others["verifydist"]=[]
    lists.setother(others)
    print("All Logs Verified")
    distdat.close()
    data.close()
    oth.close()
    others.close()
    strgnew.close()
    jsondata.close()
        
  @commands.command(name="verdist")
  async def verdist(self,ctx):
    if ctx.message.author.id in developers:
      await ctx.send("Starting Verification")
      await self.verifyscheduled(self)
      await ctx.send("Verified Distro Logs")
    else:
      await ctx.send("Only The Developer Can Use This Command.")
  @commands.command(name="verifytimer",aliases=['vft'],description="Starts Distribution Verification Timer, DEV ONLY",hidden=True)
  async def verifytimer(self,ctx,opt="timer",hrs=0,mins=5,secs=0,micsecs=0,dys=1):
    if ctx.message.author.id in developers:
      self.verifyscheduled.cancel()
      self.verifyscheduled.start()
      await ctx.send("Started Distribution Verification Timer")
    else:
      await ctx.send("Only The Developer Can Use This Command.")

  @commands.Cog.listener()
  async def on_message(self,msg):
    condat=lists.readdataE()
    if int(msg.channel.id)==condat[str(msg.guild.id)]["distchan"]:
      cnt=msg.content
      pts=cnt.split("\n")
      u=pts[1]
      users=u.split(" ")
      l=pts[2]
      loot=l.split(";")
      purp=pts[5]
      data=lists.bals()
      prebal=data[str(msg.guild.id)]["clan"]
      thrd=await msg.create_thread(name="Calculations (How Much Everyone Gets)")
      for x in loot:
        loc=loot.index(x)
        w=x.split(":")
        item=str(w[0])
        amount=int(w[1])
        percent=float(condat[str(msg.guild.id)]["clanPercent"]) #Percent The Clan Gets
        whole=amount
        pw= percent * whole
        div=round(pw/100)
        cbala=0
        print(amount)
        if amount > 0:
          cbala=data[str(msg.guild.id)]["clan"][str(item)]
          cbala=cbala+div
          await thrd.send(f"Clan Gets {div} {item}")
        else:
          cbala=0
          await thrd.send(f"Clan Gets Nothing From Withdrawls")
        if condat[str(msg.guild.id)]["storebal"].lower()=="no":
          cbala=data[str(msg.guild.id)]["clan"][str(item)]
          cbala=cbala+whole
        else:
          cbala=data[str(msg.guild.id)]["clan"][str(item)]
          cbala=cbala+div
          data[str(msg.guild.id)]["clan"][item]=cbala
        rem=amount-div
        mem=round(rem/int(len(users)))
        memtot=mem*len(users)
        await thrd.send(f'The Listed Members Get {mem} {item} each.')
        #Code To Give The "Lost" Flux To The Clan
        if div+memtot != whole:
          dim=div+memtot
          missing=whole-dim
          cbalb=cbala+missing
          data[str(msg.guild.id)]["clan"][item]=cbalb
        for i in users:
          i=i.replace("<","").replace("@","").replace(">","")
          mbr=msg.guild.get_member(int(i)).id
          keys=list(data[str(msg.guild.id)][str(mbr)].keys())
          if str(item) in keys:
            bal=data[str(msg.guild.id)][str(mbr)][str(item)]
            bal=bal+mem
            data[str(msg.guild.id)][str(mbr)][str(item)]=bal
          else:
            bala=data[str(msg.guild.id)]["clan"][str(item)]
            bala=bala+mem
            data[str(msg.guild.id)]["clan"][str(item)]=bala
      other=lists.readother()
      endbal=data[str(msg.guild.id)]["clan"]
      lootdict={}
      for x in loot:
        p=list(x.split(":"))
        lootdict.update({str(p[0]):int(p[1])})
      apit=[msg.guild.id,msg.channel.id,msg.id,prebal,endbal,msg.content,data[str(msg.guild.id)],lootdict,purp]
      other["verifydist"].append(apit)
      if condat[str(msg.guild.id)]["verbal"]=="yes":
        lists.setother(other)
        await msg.add_reaction("⬆")
      else:
        dat=lists.readdata()
        dat=data
        lists.setdata(dat)
        await msg.add_reaction("⏫")
        dat.close()
    else:
      pass
    condat.close()
    other.close()
    data.close()


  @commands.Cog.listener()
  async def on_member_update(self,before, after):
    x=0
    if x==1:
      gid = before.guild.id
      data=lists.readdata()
      condat=lists.readdataE()
      newRole = next(role for role in after.roles if role not in before.roles)
      if int(newRole.name) == condat[str(gid)]["memrole"]:
        inputv={}
        keylist=lists.readother()["defaultdist"].keys()
        if str(gid) in keylist:
          items=lists.readother()["defaultdist"][str(gid)]
          for x in items:
            inputv.update({str(x):0})
        else:
          inputv = {"flux":0,"loaders":0,"rcs":0,"pushers":0}
        data[gid][str(before.id)]=dict(inputv)
        lists.setdata(data)
      else:
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(DistCmds(bot))
  
#def workaround():
  #loop = asyncio.new_event_loop()
  #asyncio.set_event_loop(loop)
  #loop.run_until_complete(DistCmds.verifyscheduled(DistCmds))
  #loop.close()
  #asyncio.run(DistCmds.self.verifyscheduled())

    
    

#schedule.every().day.at("01:00").do(job,'It is 01:00')

#while True:
    #schedule.run_pending()
    #time.sleep(60) # wait one minute