import os, discord
import time
import asyncio
import pytz
import datetime
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Timer
import urllib.request
import requests
import gzip
#from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup

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

class DistCmds(commands.Cog, name="Distribution Commands",description="Loot Distribution Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

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
                await ctx.send(f'Now {member} has {added} {item} in {ctx.message.guild.name}')
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
          await ctx.send(dumps(lists.readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
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

  @commands.command(name="verifytimer",aliases=['vft'],description="Starts Distribution Verification Timer, DEV ONLY")
  async def verifytimer(self,ctx,opt="timer",hrs=0,mins=5,secs=0,micsecs=0,dys=1):
    if ctx.message.author.id in developers:
      if opt=="timer":
        x=datetime.today()
        tz = pytz.timezone('America/New_York')
        x=datetime.today()
        y = x.replace(day=x.day, hour=hrs, minute=mins, second=secs, microsecond=micsecs) + timedelta(days=dys)
        delta_t=y-x
        secs=delta_t.total_seconds()
        client=commands.Bot
        t = Timer(secs, verifyschedule(client))
        t.start()
      else:
        sched = BackgroundScheduler()
        sched.start()
        dt = datetime.datetime
        Future = dt.now() + datetime.timedelta(milliseconds=2000)
        job = sched.add_job(verifyschedule(self.bot), 'date', run_date=Future)
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
      #print(loot)
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
        #print(div)
        #print(cbala)
        data[str(msg.guild.id)]["clan"][item]=cbala
        lists.setdata(data)
        rem=amount-div
        #print(whole)
        #print(rem)
        mem=round(rem/int(len(users)))
        #print(mem)
        memtot=mem*len(users)
        #Code To Give The "Lost" Flux To The Clan
        if div+memtot != whole:
          dim=div+memtot
          missing=whole-dim
          cbalb=cbala+missing
          data[str(msg.guild.id)]["clan"][item]=cbalb
          #print("clanbalance")
          #print(div+missing)
          lists.setdata(data)
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
            lists.setdata(data)
          else:
            #print("False")
            bala=data[str(msg.guild.id)]["clan"][str(item)]
            #print(bala)
            bala=bala+mem
            #print(bala)
            data[str(msg.guild.id)]["clan"][str(item)]=bala
            #print(data[str(msg.guild.id)]["clan"][str(item)])
            lists.setdata(data)
      other=lists.readother()
      #print(other)
      endbal=data[str(msg.guild.id)]["clan"]
      #print(endbal)
      apit=[msg.guild.id,msg.id,prebal,endbal]
      other["verifydist"].append(apit)
      #print(other)
      lists.setother(other)
      await msg.add_reaction("⬆")
    else:
      pass


async def setup(bot: commands.Bot):
    await bot.add_cog(DistCmds(bot))
  
async def verifyschedule(bot):
  a=0
  data =lists.readdataE()
  oth=lists.readother()
  distdat=lists.readdata()
  for x in oth["verifydist"]:
    loc = oth["verifydist"].index(x)
    gid=x[0]
    msgid=x[1]
    prebal=x[2]
    endbal=x[3]
    guild=bot.get_guild(int(gid))
    mesg=bot.get_message(int(msgid))
    try:
      if str(mesg.guild.id) in list(data.keys()):
        distro=int(data[str(mesg.guild.id)]["distchan"])
        if int(mesg.channel.id)==distro:
          print(1)
          pts=mesg.split("\n")
          date=pts[3].split("/")
          hex=str("{"+str(pts[2])+"}")
          distship=str("{"+data[str(mesg.guild.id)]["distship"]+"}")
          strgnew=lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{date[2]}_{date[0]}_{date[1]}/ships.json.gz')
          strgold=lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{int(int(date[2])-1)}_{int(int(date[0])-1)}_{int(int(date[1])-1)}/ships.json.gz')
          jsondata = lists.get_gzipped_json(f'https://pub.drednot.io/prod/econ/{date[2]}_{date[0]}_{date[1]}/log.json.gz')
          def find_routea(data, route_no):
            return list(filter(lambda x: x.get("src") == route_no, data))
          route = find_routea(jsondata,hex)
          remain=list(filter(lambda x: x.get("dst") == distship, route))
          for x in route:
            if x["dst"]==str(distship) and x["src"]==str(hex):
              cbal=list(filter(lambda x: x.get(str(hex)) == distship, strgold))
              formbal=lists.formatClanBal(cbal,endbal)
              if str(endbal) == str(formbal):
                await mesg.add_reaction("✅")
              else:
                await mesg.add_reaction("❌")   
        else:
          pass
      else:
        pass
      oth["verifydist"].remove(x)
    except:
      await mesg.add_reaction("🙅")

    
      
x=datetime.today()
tz = pytz.timezone('America/New_York')
x=datetime.today()
y = x.replace(day=x.day, hour=0, minute=5, second=0, microsecond=0) + timedelta(days=1)
delta_t=y-x

secs=delta_t.total_seconds()
client=commands.Bot
#t = Timer(secs, verifyschedule(client))
#t.start()

#schedule.every().day.at("01:00").do(job,'It is 01:00')

#while True:
    #schedule.run_pending()
    #time.sleep(60) # wait one minute