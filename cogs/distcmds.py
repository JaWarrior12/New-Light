import os, discord
import time as timea
import asyncio
import pytz
import datetime
from datetime import datetime, timedelta, timezone
from datetime import time as tme
from apscheduler.schedulers.background import BackgroundScheduler
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
from dpyConsole import Console

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

  @commands.command(name="logloot",brief="Adds/Subtracts loot from a user's balance.",help="Adds/Subtracts from a user's balance. The format is: n!logloot @User item amount. If you are subtracting make the amount negative.")
  async def returnpaymentdata(self, ctx, member, item, amount):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        msgb = str(member)+" "+item+" "+amount
        lists.logback(ctx,msgb)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        if member=="clan":
          pass
        else:
          member=int(member.replace("<","").replace("@","").replace(">",""))
          member=ctx.message.guild.get_member(member).id
        try:
          nf = int(dumps(lists.readdata()[gid][str(member)][str(item)]).replace(':','=').replace('{','').replace('}','').replace('"',''))
          ns = int(amount)
          added = ns + nf
          if chk == True:
                data[gid][str(member)][str(item)] = int(added)
                lists.setdata(data)
                await ctx.send(f'Now {member.name} has {added} {item} in {ctx.message.guild.name}')
        except KeyError:
          await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
          
  @commands.command(name='reset',help="Resets one loot value in a user's balance. Format: n!reset @User item")
  async def resetalldata(self, ctx, member: discord.Member, item):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        msgb=str(member)+" "+item
        lists.logback(ctx,msgb)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        if chk == True:
          try:
            data[gid][str(member.id)][str(item)]=0
            lists.setdata(data)
            await ctx.send('User Data Reset')
          except KeyError:
            await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
        else:
          return False
          
  @commands.command(name='balance',brief="Calls a user's balance.",help="Calls a member's balance. Just ping the user in the command. Format: n!balance @user")
  async def getuserloot(self,ctx,member: discord.Member):
    if str(ctx.message.author.id) not in banned:
      data = None
      print(member.id)
      #chk = lists.checkperms(ctx)
      gid = str(ctx.message.guild.id)
      lists.logback(ctx,member)
      #if chk == True:
      try:
        await ctx.send(dumps(lists.readdata()[gid][str(member.id)]).replace(':','=').replace('{','').replace('}','').replace('"',''))
      except KeyError:
        await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
    elif str(ctx.message.author.id) in banned:
      await ctx.send("Your ID Is In The Banned List.")
    else:
      await ctx.send("Error")

  @commands.command(name="addmember",brief="Adds a member to the clan's distribution database.", help="Adds a member to the distribution database. Just ping the user in the command. Format: n!addmember @User")
  async def addmember(self,ctx, member: discord.Member):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        lists.logback(ctx,member)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        if chk == True:
          inputv={}
          keylist=lists.readother()["defaultdist"].keys()
          await ctx.send(keylist)
          if str(ctx.message.guild.id) in keylist:
            items=lists.readother()["defaultdist"][str(ctx.message.guild.id)]
            for x in items:
              inputv.update({str(x):0})
          else:
            inputv = {"flux":0,"loaders":0,"rcs":0,"pushers":0}
          data[gid][str(member.id)]=dict(inputv)
          lists.setdata(data)
          await ctx.send(f'Added {member} to the distribution list in {ctx.message.guild.name}')
        else:
          return False

  @commands.command(name="removemember",brief="Removes a member from a clan's distribution database.", help="Removes a member from the distribution database. Just ping the user in the command and it will remove them. Format: n!removemember @User")
  async def remmem(self,ctx,member: discord.Member):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        mem=str(member.id)
        del data[gid][mem]
        lists.logback(ctx,member)
        if chk == True:
          try:
            lists.setdata(data)
            await ctx.send(f'Removed {member} from the distribution list in {ctx.message.guild.name}')
          except KeyError:
            await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
        else:
          return False

  @commands.command(name='balall',help="Calls all balances in a clan's distribution database. Format: n!balall")
  async def balanceall(self,ctx):
        clan = ctx.message.guild
        #msgparts, data = msg.split(" "), lists.readdata()
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        lists.logback(ctx,clan)
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
          return False

  @commands.command(name="defaultbal",description="Sets the default balance, enter each item separated by a semi-colon (;). Ex. flux;rubber;loaders;rcs")
  async def defaultbal(self,ctx,*,items):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      lists.logback(ctx,items)
      if chk == True:
        list=items.split(";")
        data=lists.readother()
        data["defaultdist"][str(ctx.message.guild.id)]=list
        lists.setother(data)
        await ctx.send("Updated Default Balance")
      else:
        await ctx.send("Unauhtorized To Use Leadership Commands")
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
    
  @tasks.loop(time=tmes)
  #@self.my_console.command()
  async def verifyscheduled(self):
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
      guild=self.bot.get_guild(int(gid))
      channel=guild.get_channel(chanid)
      #task = asyncio.create_task(channel.fetch_message(int(msgid)))
      #mesg=await asyncio.shield(task)
      mesg=await channel.fetch_message(int(msgid))
      #print(mesg)
      try:
        #print(7)
        if str(mesg.guild.id) in list(data.keys()):
          distro=int(data[str(mesg.guild.id)]["distchan"])
          #print(distro)
          if int(mesg.channel.id)==distro:
            #print(1)
            pts=ctxt.split("\n")
            pts=list(pts)
            #print(pts)
            date=pts[4].split("/")
            #print(date)
            hex=str("{"+str(pts[3])+"}")
            #print(hex)
            ds=data[str(mesg.guild.id)]["distship"]
            distship=str("{"+ds+"}")
            distshipb=ds
            #print(distship)
            strgnew=lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{date[2]}_{date[0]}_{date[1]}/ships.json.gz')
            #print(4)
            #strgold=lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{int(int(date[2])-1)}_{int(int(date[0])-1)}_{int(int(date[1])-1)}/ships.json.gz')
            #print(2)
            jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{date[2]}_{date[0]}_{date[1]}/log.json.gz')
            #print(6)
            def find_routea(data, route_no):
              return list(filter(lambda x: x.get("src") == route_no, data))
            route = find_routea(jsondata,hex)
            remain=list(filter(lambda x: x.get("dst") == distship, route))
            #print(9)
            #print(remain)
            count=0
            result=0
            for f in remain:
              #print(f)
              #print(f['src'])
              #print(f['dst'])
              hexa=hex
              distshipa=distship
              #print(hexa)
              #print(distshipa)
              if f['dst']==distshipa and f['src']==hexa:
                cbal=list(filter(lambda f: f.get('hex_code') == ds, strgnew))
                #print(cbal)
                #print(10)
                #print(cbal[0]['items'])
                formbal=lists.formatClanBal(cbal[0]['items'],endbal)
                #print(formbal)
                #print(8)
                if str(endbal) == str(formbal):
                  result=1
                  #await mesg.add_reaction("✅")
                  #oth["verifydist"].remove(x)
                  #lists.setother(oth)
                else:
                  result=2
                  #await mesg.add_reaction("❌")
                  #print(oth)
                  #oth["verifydist"].remove(x)
                  #lists.setother(oth)
                  #distdat[str(mesg.guild.id)]=x[6]
                  #lists.setdata(distdat)
              else:
                await mesg.add_reaction("✖")
            #print(result)
            if result==1:
              await mesg.add_reaction("✅")
              #print(x[6])
              distdat[str(mesg.guild.id)]=x[6]
              lists.setdata(distdat)
              others=lists.readother()
              others["verifydist"].remove(x)
              lists.setother(others)
            else:
              await mesg.add_reaction("❌")
              others=lists.readother()
              others["verifydist"].remove(x)
              lists.setother(others)
            print("Reaction Added")
          else:
            pass
        else:
          pass
        oth["verifydist"].remove(x)
      except:
        await mesg.add_reaction("🤷")
        others=lists.readother()
        others["verifydist"].remove(x)
        lists.setother(others)
        print("Error Occured")


  @commands.command(name="verifytimer",aliases=['vft'],description="Starts Distribution Verification Timer, DEV ONLY")
  async def verifytimer(self,ctx,opt="timer",hrs=0,mins=5,secs=0,micsecs=0,dys=1):
    if ctx.message.author.id in developers:
      #await self.verifyscheduled()
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
      #print(users)
      l=pts[2]
      loot=l.split(";")
      data=lists.readdata()
      prebal=data[str(msg.guild.id)]["clan"]
      #allbal=data[str(msg.guild.id)]["clan"]
      #print(loot)
      thrd=await msg.create_thread(name="Calculations (How Much Everyone Gets")
      for x in loot:
        loc=loot.index(x)
        w=x.split(":")
        item=str(w[0])
        amount=int(w[1])
        #print(item)
        percent=float(condat[str(msg.guild.id)]["clanPercent"]) #Percent The Clan Gets
        whole=amount
        pw= percent * whole
        #pw=round(pa/100)
        #print(pw)
        div=round(pw/100)
        cbala=data[str(msg.guild.id)]["clan"][str(item)]
        cbala=cbala+div
        await thrd.send(f"Clan Gets {div} {item}")
        if condat[str(msg.guild.id)]["storebal"].lower()=="yes":
          cbala=data[str(msg.guild.id)]["clan"][str(item)]
          cbala=cbala+whole
        else:
          cbala=data[str(msg.guild.id)]["clan"][str(item)]
          cbala=cbala+div
        #print(div)
        #print(cbala)
        data[str(msg.guild.id)]["clan"][item]=cbala
        #lists.setdata(data)
        rem=amount-div
        #print(whole)
        #print(rem)
        mem=round(rem/int(len(users)))
        #print(mem)
        memtot=mem*len(users)
        await thrd.send(f'The Listed Members Get {mem} {item} each.')
        #Code To Give The "Lost" Flux To The Clan
        if div+memtot != whole:
          dim=div+memtot
          missing=whole-dim
          cbalb=cbala+missing
          data[str(msg.guild.id)]["clan"][item]=cbalb
          #print("clanbalance")
          #print(div+missing)
          #lists.setdata(data)
        #print(users)
        for i in users:
          #print(i)
          i=i.replace("<","").replace("@","").replace(">","")
          #print(i)
          i=msg.guild.get_member(int(i)).id
          #print(i)
          keys=list(data[str(msg.guild.id)][str(i)].keys())
          if str(item) in keys:
            bal=data[str(msg.guild.id)][str(i)][str(item)]
            #print(bal)
            #keys=list(data[str(msg.guild.id)][str(i)].keys())
            #print(keys)
            #print(item)
            #print(mem)
          #if str(item) in keys:
            #print("True")
            bal=bal+mem
            #print(bal)
            data[str(msg.guild.id)][str(i)][str(item)]=bal
            #print(data[str(msg.guild.id)][str(i)][str(item)])
            #lists.setdata(data)
          else:
            #print("False")
            bala=data[str(msg.guild.id)]["clan"][str(item)]
            #print(bala)
            bala=bala+mem
            #print(bala)
            data[str(msg.guild.id)]["clan"][str(item)]=bala
            #print(data[str(msg.guild.id)]["clan"][str(item)])
            #lists.setdata(data)
      other=lists.readother()
      #print(other)
      endbal=data[str(msg.guild.id)]["clan"]
      #print(endbal)
      apit=[msg.guild.id,msg.channel.id,msg.id,prebal,endbal,msg.content,data[str(msg.guild.id)]]
      other["verifydist"].append(apit)
      #print(other)
      lists.setother(other)
      await msg.add_reaction("⬆")
    else:
      pass


  @commands.Cog.listener()
  async def on_ready(self):
    x=datetime.today()
    tz = pytz.timezone('America/New_York')
    x=datetime.today()
    y = x.replace(day=x.day, hour=16, minute=15, second=0, microsecond=0) + timedelta(days=0)
    delta_t=y-x
    secs=delta_t.total_seconds()
    print(secs)
    #client=commands.Bot
    t = Timer(10, self.workaround)
    t.start()
    print("Started Timer")

  @commands.Cog.listener()
  async def on_member_update(self,before, after):
    if len(before.roles) < len(after.roles):
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