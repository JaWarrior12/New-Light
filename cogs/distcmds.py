import os, discord
from aiohttp import DataQueue
import time as timea
import traceback
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
from startup import startup
#from dpyConsole import Console

#Lists
import lists
#Auth For Leadership Commands
#authorized = lists.authorized
banned = lists.banned
developers = lists.developers


#tz = pytz.timezone('America/New_York')
utc=timezone.utc
tmes=tme(hour=0,minute=20,tzinfo=utc)

class DistCmds(commands.Cog, name="Distribution Commands",description="Loot Distribution Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    #self.verifyschedule.start()
    #self.my_console=Console(bot)
  def cog_unload(self):
    #self.verifyschedule.cancel()
    pass
    
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
  async def returnpaymentdata(self, ctx, member, item, amount,*,reason=None):
          msg="a b"
          msgparts, data = msg.split(" "), lists.readdata()
          msgb = str(member)+" "+item+" "+amount
          #lists.logback(ctx,msgb)
          chk = lists.checkperms(ctx)
          gid = str(ctx.message.guild.id)
          added=0
          memvar=0
          memName=0
          memAv=0
          memMem=0
          try:
            member=await commands.MemberConverter().convert(ctx,member)
          except:
            member=member
          if type(member) is discord.Member:
            memvar=member.id
            memName=member.display_name
            memAv=member.display_avatar
            memMen=member.mention
          else:
            memvar=member
            memName=member
            memAv=None
            memMen=member
          #try:
          if chk == True:
            previousBalance=data[gid][str(memvar)].copy()
            if item in lists.readother()["alloweditems"]:
              if item in list(data[gid][str(memvar)].keys()):
                nf = int(data[gid][str(memvar)][item])
                ns = int(amount)
                added = ns + nf
              else:
                nf = 0
                ns = int(amount)
                added = ns + nf
              data[gid][str(memvar)].update({str(item):int(added)})
              lists.setdata(data)
              #await ctx.send(f'Now {member.name} has {added} {item} in {ctx.message.guild.name}')
              e = discord.Embed(title="Member Balance Update")
              e.add_field(name="Target Member", value=memName, inline=True)
              e.add_field(name="Updated By", value=ctx.message.author.display_name, inline=True)
              e.add_field(name="Old Balance",value=nf,inline=True)
              e.add_field(name="New Balance",value=added,inline=True)
              e.add_field(name="Item",value=item,inline=True)
              e.add_field(name="Amount Added",value=ns,inline=True)
              e.set_thumbnail(url=memAv)
              #tz = pytz.timezone('America/New_York')
              e.timestamp=datetime.now()
              await ctx.send(embed=e)
              myguild = self.bot.get_guild(1031900634741473280)
              mychannel = myguild.get_channel(1145862891271094322)
              await mychannel.send(f"{memMen}'s balance was changed by `{ns}` `{item}`.\nPerformed By: {ctx.message.author.mention}\nPerformed At: `{datetime.now()}`\nReason: `{reason}`\nPerformed In Server: `{ctx.message.guild.name}`")
              await mychannel.send(f"Previous Balance: `{previousBalance}`\nResulting Balance: `{data[gid][str(memvar)]}`")
            else:
              await ctx.send(f"Sorry Item `{item}` is not registered in my system. Please see https://discord.com/channels/1031900634741473280/1145413798153437264 for the item name reference list.")
          else:
            await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")
          #except KeyError:
            #await ctx.send(f"KeyError: Either Item {item} Or User {member} cannot be found in {ctx.message.guild.name}'s Distribution List.")
          
  @commands.command(name='reset',brief="Resets a member's balance. (LR)",help="Resets one loot value in a user's balance. Format: n!reset @User item")
  async def resetalldata(self, ctx, member, item,*,reason=None):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        msgb=str(member)+" "+item
        #lists.logback(ctx,msgb)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        memvar=0
        memName=0
        memAv=0
        memMen=0
        try:
          member=await commands.MemberConverter().convert(ctx,member)
        except:
          member=member
        if type(member) is discord.Member:
          memvar=member.id
          memName=member.display_name
          memAv=member.display_avatar
          memMen=member.mention
        else:
          memvar=member
          memName=member
          memAv=None
          memMen=member
        if chk == True:
          try:
            previousBalance=data[gid][str(memvar)].copy()
            if item in lists.readother()["alloweditems"]:
              data[gid][str(memvar)][str(item)]=0
              lists.setdata(data)
              e = discord.Embed(title="Member Balance Reset")
              e.add_field(name="Target Member", value=memName, inline=True)
              e.add_field(name="Reset By", value=ctx.message.author.display_name, inline=True)
              e.add_field(name="Item",value=item,inline=True)
              e.add_field(name="Previous Balance",value=previousBalance[item],inline=True)
              e.set_thumbnail(url=memAv)
              #tz = pytz.timezone('America/New_York')
              e.timestamp=datetime.now()
              await ctx.send(embed=e)
              myguild = self.bot.get_guild(1031900634741473280)
              mychannel = myguild.get_channel(1145862891271094322)
              await mychannel.send(f"{memMen}'s balance was changed, item `{item}` was reset.\nPerformed By: {ctx.message.author.mention}\nPerformed At: `{datetime.now()}`\nReason: `{reason}`\nPerformed In Server: `{ctx.message.guild.name}`")
              await mychannel.send(f"Previous Balance: `{previousBalance}`\nResulting Balance: `{data[gid][str(memvar)]}`")
            else:
              await ctx.send(f"Sorry Item `{item}` is not registered in my system. Please see https://discord.com/channels/1031900634741473280/1145413798153437264 for the item name reference list.")
          except KeyError:
            await ctx.send(f"KeyError: Either Item {item} Or User {member} cannot be found in {ctx.message.guild.name}'s Distribution List.")
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")

  @commands.command(name='deleteitem',brief="Deletes An Item From A User's Balance. (LR)",help="Deletes one loot value in a user's balance. Format: n!deleteitem @User item")
  async def deleteiteminbalance(self, ctx, member, item,*,reason=None):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        msgb=str(member)+" "+item
        #lists.logback(ctx,msgb)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        memvar=0
        memName=0
        memAv=0
        memMen=0
        try:
          member=await commands.MemberConverter().convert(ctx,member)
        except:
          member=member
        if type(member) is discord.Member:
          memvar=member.id
          memName=member.display_name
          memAv=member.display_avatar
          memMen=member.mention
        else:
          memvar=member
          memName=member
          memAv=None
          memMen=member
        if chk == True:
          try:
            previousBalance=data[gid][str(memvar)].copy()
            if item in lists.readother()["alloweditems"]:
              data[gid][str(memvar)].pop(item)
              lists.setdata(data)
              e = discord.Embed(title="Member Balance Item Deletion")
              e.add_field(name="Target Member", value=memName, inline=True)
              e.add_field(name="Deleted By", value=ctx.message.author.display_name, inline=True)
              e.add_field(name="Item Deleted",value=item,inline=True)
              e.add_field(name="Previous Balance",value=previousBalance[item],inline=True)
              e.set_thumbnail(url=memAv)
              #tz = pytz.timezone('America/New_York')
              e.timestamp=datetime.now()
              await ctx.send(embed=e)
              myguild = self.bot.get_guild(1031900634741473280)
              mychannel = myguild.get_channel(1145862891271094322)
              await mychannel.send(f"`{memMen}'s balance was changed, item `{item}` was deleted.\nPerformed By: {ctx.message.author.mention}\nPerformed At: `{datetime.now()}`\nReason: `{reason}`\nPerformed In Server: `{ctx.message.guild.name}`")
              await mychannel.send(f"Previous Balance: `{previousBalance}`\nResulting Balance: `{data[gid][str(memvar)]}`")
            else:
              await ctx.send(f"Sorry Item `{item}` is not registered in my system. Please see https://discord.com/channels/1031900634741473280/1145413798153437264 for the item name reference list.")
          except KeyError:
            await ctx.send(f"KeyError: Either Item {item} Or User {member} cannot be found in {ctx.message.guild.name}'s Distribution List.")
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")

  @commands.command(name='balance',brief="Calls a user's balance.",help="Calls a member's balance. Just ping the user in the command. Format: n!balance @user")
  async def getuserloot(self,ctx,member):
    if str(ctx.message.author.id) not in banned:
      data = None
      #chk = lists.checkperms(ctx)
      gid = str(ctx.message.guild.id)
      #lists.logback(ctx,member)
      #if chk == True:
      data = lists.readdata()
      memvar=0
      memName=0
      memAv=0
      memMen=0
      if member=="clan":
        memvar=member
        memName=member
        memAv=None
        memMen=member
      else:
        try:
          member=await commands.MemberConverter().convert(ctx,member)
        except:
          member=member
        if type(member) is discord.Member:
          memvar=member.id
          memName=member.display_name
          memAv=member.display_avatar
          memMen=member.mention
        else:
          memvar=member
          memName=member
          memAv=None
          memMen=member
      try:
        e = discord.Embed(title="Member Balance")
        e.add_field(name="Member", value=memName, inline=True)
        for x in data[gid][str(memvar)].keys():
          e.add_field(name=x,value=data[gid][str(memvar)][x],inline=True)
        e.set_thumbnail(url=memAv)
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
  async def addmember(self,ctx, member):
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdata()
        #lists.logback(ctx,member)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        memvar=0
        memName=0
        memAv=0
        memMen=0
        try:
          member=await commands.MemberConverter().convert(ctx,member)
        except:
          member=member
        if type(member) is discord.Member:
          memvar=member.id
          memName=member.display_name
          memAv=member.display_avatar
          memMen=member.mention
        else:
          memvar=member
          memName=member
          memAv=None
          memMen=member
        if chk == True:
          inputv={}
          keylist=lists.readother()["defaultdist"].keys()
          #await ctx.send(keylist)
          if str(ctx.message.guild.id) in keylist:
            items=lists.readother()["defaultdist"][str(ctx.message.guild.id)]
            for x in items:
              inputv.update({str(x):0})
          else:
            inputv = {"flux":0,"loader":0,"rc":0,"pusher":0}
          data[gid][str(memvar)]=dict(inputv)
          lists.setdata(data)
          e = discord.Embed(title="Member Added")
          e.add_field(name="Member", value=memName, inline=True)
          e.add_field(name="Added By",value=ctx.message.author.display_name,inline=True)
          e.add_field(name="Default Balance",value=inputv,inline=True)
          e.set_thumbnail(url=memAv)
          #tz = pytz.timezone('America/New_York')
          e.timestamp=datetime.now()
          await ctx.send(embed=e)
          myguild = self.bot.get_guild(1031900634741473280)
          mychannel = myguild.get_channel(1145862891271094322)
          await mychannel.send(f"`{memMen}` was added to the distribution list in server `{ctx.message.guild.name}`.\nPerformed By: {ctx.message.author.mention}\nPerformed At: `{datetime.now()}`\nReason: `Add Member`\nPerformed In Server: `{ctx.message.guild.name}`")
          await mychannel.send(f"Resulting Balance: `{data[gid][str(memvar)]}`")
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")

  @commands.command(name="removemember",brief="Removes a member from a clan's distribution database. (LR)", help="Removes a member from the distribution database. Just ping the user in the command and it will remove them. Format: n!removemember @User")
  async def remmem(self,ctx,member,*,reason=None):
    msg="a b"
    msgparts, data = msg.split(" "), lists.readdata()
    chk = lists.checkperms(ctx)
    gid = str(ctx.message.guild.id)
    memvar=0
    memName=0
    memAv=0
    memMen=0
    try:
      member=await commands.MemberConverter().convert(ctx,member)
    except:
      member=member
    if type(member) is discord.Member:
      memvar=str(member.id)
      memName=member.display_name
      memAv=member.display_avatar
      memMen=member.mention
    else:
      memvar=member
      memName=member
      memAv=None
      memMen=member
    myguild = self.bot.get_guild(1031900634741473280)
    mychannel = myguild.get_channel(1145862891271094322)
    #lists.logback(ctx,member)
    if chk == True:
      try:
        lists.setdata(data)
        memvar=member
        e = discord.Embed(title="Member Removed")
        e.add_field(name="Member", value=memName, inline=True)
        e.add_field(name="Removed By By",value=ctx.message.author.display_name,inline=True)
        e.add_field(name="Reason",value=reason,inline=True)
        e.set_thumbnail(url=memAv)
        #tz = pytz.timezone('America/New_York')
        e.timestamp=datetime.now()
        await ctx.send(embed=e)
        previousBalance=data[gid][memvar].copy()
        await mychannel.send(f"`{memMen}` was removed from the distribution list in server `{ctx.message.guild.name}`.\nPerformed By: {ctx.message.author.mention}\nPerformed At: `{datetime.now()}`\nReason: `Remove Member`\nPerformed In Server: `{ctx.message.guild.name}`")
        await mychannel.send(f"Balance Before Deletion: `{previousBalance}`")
        del data[gid][memvar]
        lists.setdata(data)
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
          ids = [member.id for member in ctx.guild.members]
          for x in memlist:
            if x == "clan" or x not in ids:
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

  @commands.command(name="defaultbalance",aliases=["defaultbal"],brief="Sets a clan's default balance (LR)",help="Sets the default balance, enter each item separated by a semi-colon (;). Ex. flux;rubber;loaders;rcs",description="Sets the default balance when adding new members.")
  async def defaultbal(self,ctx,*,items):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      #lists.logback(ctx,items)
      if chk == True:
        allowitems=[]
        blockitems=[]
        defballist=items.split(";")
        try:
          for x in defballist:
            if x in lists.readother()["alloweditems"]:
              allowitems.append(x)
            else:
              blockitems.append(x)
        except Exception as e:
          print(e)
        data=lists.readother()
        data["defaultdist"][str(ctx.message.guild.id)]=allowitems
        lists.setother(data)
        if len(blockitems)==0:
          e = discord.Embed(title="Default Balance Updated")
          e.add_field(name="Updated By",value=ctx.message.author.display_name,inline=True)
          e.add_field(name="Default Balance",value=defballist,inline=True)
          e.set_thumbnail(url=ctx.message.author.display_avatar)
          #tz = pytz.timezone('America/New_York')
          e.timestamp=datetime.now()
          await ctx.send(embed=e)
          users=lists.readdata()
          for user in list(users[str(ctx.message.guild.id)].keys()):
            userItems=list(users[str(ctx.message.guild.id)][user].keys())
            for itemKey in allowitems:
              print(itemKey)
              if itemKey not in userItems:
                users[str(ctx.message.guild.id)][user].update({itemKey:0})
          lists.setdata(users)
          await ctx.send("All Member Balances Updated If They Did Not Contain Items From The New Default Balance")
        else:
          e = discord.Embed(title="Default Balance Updated")
          e.add_field(name="Updated By",value=ctx.message.author.display_name,inline=True)
          e.add_field(name="Default Balance",value=defballist,inline=True)
          e.add_field(name="Allowed Items",value=allowitems)
          e.add_field(name="Blocked Items",value=blockitems,inline=True)
          e.set_thumbnail(url=ctx.message.author.display_avatar)
          #tz = pytz.timezone('America/New_York')
          e.timestamp=datetime.now()
          await ctx.send(embed=e)
          await ctx.send(f"Sorry The Following Items: {blockitems} are not registered in my system. Please see https://discord.com/channels/1031900634741473280/1145413798153437264 for the item name reference list.")
          users=lists.readdata()
          for user in list(users[str(ctx.message.guild.id)].keys()):
            userItems=list(users[str(ctx.message.guild.id)][user].keys())
            for itemKey in allowitems:
              print(itemKey)
              if itemKey not in userItems:
                users[str(ctx.message.guild.id)][user].update({itemKey:0})
          lists.setdata(users)
          await ctx.send("All Member Balances Updated If They Did Not Contain Items From The New Default Balance")
      else:
        await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")
    else:
      await ctx.send("Your ID Is In The Banned List.")

  @commands.command(name="transfer",brief="Transfer Loot From Your Balance To Someone Else's Balance",help="Transfer Loot From Your Balance To Someone Else's Balance",description="Transfer Loot From Your Balance To Someone Else's Balance")
  async def itemTransfer(self,ctx,destination,item,amount : int,*,reason=None):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      member=destination
      memvar=0
      memName=0
      memAv=0
      memMen=0
      try:
        member=await commands.MemberConverter().convert(ctx,member)
      except:
        member=member
      if type(member) is discord.Member:
        memvar=str(member.id)
        memName=member.display_name
        memAv=member.display_avatar
        memMen=member.mention
      else:
        memvar=member
        memName=member
        memAv=None
        memMen=member
      gid=str(ctx.message.guild.id)
      myguild = self.bot.get_guild(1031900634741473280)
      mychannel = myguild.get_channel(1145862891271094322)
      if chk:
        if item in lists.readother()["alloweditems"]:
          data=lists.readdata()
          sourcePreBal=data[gid][str(ctx.message.author.id)][item]
          destPreBal=data[gid][str(memvar)][item]
          sourcePostBal=int(sourcePreBal)-int(amount)
          destPostBal=int(destPreBal)+int(amount)
          data[gid][str(ctx.message.author.id)][item]=sourcePostBal
          data[gid][memvar][item]=destPostBal
          await ctx.send(f"Transfered {amount} {item} From {ctx.message.author.mention} to {memMen}.\n- {ctx.message.author.mention}'s New Balance: {sourcePostBal}.\n- {memMen}'s New Balance: {destPostBal}.")
          lists.setdata(data)
          await mychannel.send(f"ITEM TRANSFER\n\n`{memMen}`'s Balance Was Updated by `{amount}` `{item}` `{ctx.message.guild.name}`.\nPerformed By: {ctx.message.author.mention}\nPerformed At: `{datetime.now()}`\nReason: `{reason}`\nPerformed In Server: `{ctx.message.guild.name}`")
          await mychannel.send(f"{ctx.message.author.mention}'s Balance Before Transfer: `{sourcePreBal}`")
          await mychannel.send(f"{ctx.message.author.mention}'s Balance After Transfer: `{sourcePostBal}`")
          await mychannel.send(f"{memMen}'s Balance Before Transfer: `{destPreBal}`")
          await mychannel.send(f"{memMen}'s Balance After Transfer: `{destPostBal}`")
          await mychannel.send("\nEND TRANSFER LOG")
        else:
          await ctx.send("You Can't Give That Item! Please See https://discord.com/channels/1031900634741473280/1145413798153437264 For The List Of Approved Items")
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

  @staticmethod
  async def verifyDistroLogs(self):
    print("Verifying Distro Logs")
    a=0
    data=lists.readdataE()
    oth=lists.readother()
    distdat=lists.readdata()
    dailyData=oth["verifydist"]
    print(dailyData)
  
    def findRelatingLogs(data, key, hex):
      return list(filter(lambda x: x.get(key) == hex, data))

    shipItemTotals={}
    for message in dailyData:
      result=True
      count=0
      while result and count < 1:
        #print(message)
        guild=self.bot.get_guild(int(message["guildId"]))
        channel=guild.get_channel(int(message["channelId"]))
        mesg=await channel.fetch_message(int(message["msgId"]))
        thread=guild.get_thread(int(message["thrdId"]))
        #print(thread.name)
        result=0
        try:
          #print(message)
          if str(message["sourceShip"]) not in list(shipItemTotals.keys()):
            shipItemTotals.update({message["sourceShip"]:{}})
          #print(message)
          date=f"{message['date'][2]}_{message['date'][0]}_{message['date'][1]}"
          logFile = f"https://pub.drednot.io/prod/econ/{date}/log.json.gz"
          shipFile = f"https://pub.drednot.io/prod/econ/{date}/ships.json.gz"
          
          log_response = requests.get(logFile)
          log_data = gzip.decompress(log_response.content)  #.decode('utf-8')
          logItems = loads(log_data)
        
          ships_response = requests.get(shipFile)
          shipsData = gzip.decompress(ships_response.content).decode('utf-8')
          ships= loads(shipsData)
        
          total_transfer_amount = 0
          
          logList=findRelatingLogs(logItems,"src",message["sourceShip"])
          negativeList=findRelatingLogs(logItems,"dst",message["sourceShip"])
          for sortlog in logList:
            #print(f'Src: {sortlog["src"]}; Dst: {sortlog["dst"]}')
            if sortlog["dst"] == message["destinationShip"]:
              pass
            else:
              #print(f'Removed')
              logList.remove(sortlog)
          for sortlog in negativeList:
            #print(f'Src: {sortlog["src"]}; Dst: {sortlog["dst"]}')
            if sortlog["src"] == message["destinationShip"]:
              pass
            else:
              #print(f'Removed')
              negativeList.remove(sortlog)
          lootTotals={}
          for lootItem in message["userClaim"]:
            #print(lootItem)
            if str(lootItem) not in list(shipItemTotals[message["sourceShip"]].keys()):
              shipItemTotals[message["sourceShip"]].update({str(lootItem):0})
            #print(f"lootItem: {lootItem}")
            itemTotal=0
            itemId=lists.itemNameToID(lootItem)
            for itemlog in findRelatingLogs(logList,"item",itemId):
              if int(itemlog["item"])==int(itemId) and itemlog["dst"]==message["destinationShip"]:
                itemTotal+=itemlog["count"]
                #print(itemlog)
            for itemlog in findRelatingLogs(negativeList,"item",itemId):
              if int(itemlog["item"])==int(itemId) and itemlog["src"]==message["destinationShip"]:
                itemTotal-=itemlog["count"]
                #print(itemlog)
            shipItemTotals[message["sourceShip"]][str(lootItem)]+=itemTotal
            lootTotals.update({lootItem:itemTotal})
          #print(f"ShipItemTotals: {shipItemTotals}")
          #print(f"lootTotals: {lootTotals}")
          for key in list(lootTotals.keys()):
            index=list(lootTotals.keys())
            #print(f"User Claim: key == {key}; amount == {message['userClaim'][key]}")
            #print(f"Actual: key == {key}; amount == {lootTotals[key]}")
            if message['userClaim'][key] == lootTotals[key]:
              await thread.send(f"Log Verified; Exact Amount Transferred. \nItem: `{key}`\nAmount Actually Transferred: `{lootTotals[key]}`\nItem: `{key}`\nAmount Claimed To Be Transferred: `{message["userClaim"][key]}`")
              result=1
            elif message['userClaim'][key] > lootTotals[key]:
              await thread.send(f"Log Verified; More Than Amount Listed Has Been Transferred. \nItem: `{key}`\nAmount Actually Transferred: `{lootTotals[key]}`\nItem: `{key}`\nAmount Claimed To Be Transferred: `{message["userClaim"][key]}`\nDifference: `{abs(message["userClaim"][key]-lootTotals[key])}`")
              await thread.send(f"This Is Most Likely Caused By Multiple Transfers From One Ship")
              result=True
            elif message['userClaim'][key] < lootTotals[key]:
              await thread.send(f"Log Failed Verification; Less Than Amount Listed Has Been Transferred. \nItem: `{key}`\nAmount Actually Transferred: `{lootTotals[key]}`\nItem: `{key}`\nAmount Claimed To Be Transferred: `{message["userClaim"][key]}`\nDifference: `{abs(message["userClaim"][key]-lootTotals[key])}`")
              #thread.send(f"This Is Most Likely Caused By")
              result=False
        except Exception as e:
          print(e)
          if hasattr(e, 'message'):
            emes=e.message
          else:
            emes=e
          print(emes)
          print(traceback.format_exc())
          await mesg.add_reaction("🤷")
          print("Error Occured")
        count+=1
      if result:
        await mesg.add_reaction("✅")
        distdat[str(mesg.guild.id)]=message["clanData"]
        lists.setdata(distdat)
      else:
        await mesg.add_reaction("❌")
      print("Reaction Added")
  #else:
    #pass
      oth["verifydist"].remove(message)
    others=lists.readother()
    others["verifydist"]=[]
    lists.setother(others)
    print("All Logs Verified")

  @tasks.loop(time=tmes)
  async def verifyschedule(self):
    await self.verifyDistroLogs(self)

  @commands.command(name="forceDistroVerification",aliases=["fdl"])
  async def forceDistroVerification(self,ctx):
    if ctx.message.author.id in developers:
      await ctx.send("Forcefully Verifying Distro Logs")
      await self.verifyDistroLogs(self)
      await ctx.send("Distro Logs Verified")
  
  @commands.command(name="listDistroVerificationLogs",aliases=["ldl","ldvl"])
  async def listDistroVerificationLogs(self,ctx):
    if ctx.message.author.id in developers:
      data = lists.readother()["verifydist"]
      await ctx.send(f"Length Of Log List: {len(data)}")
      for x in data:
        await ctx.send(x)

  @commands.command(name="forceClearDistroVerification",aliases=["fcdl"])
  async def forceClearDistroVerification(self,ctx):
    if ctx.message.author.id in developers:
      await ctx.send("Forcefully Cearing Distro Verification Logs")
      data = lists.readother()
      await ctx.send(f"Number of Logs Being Cleared: {len(data["verifydist"])}\nLogs:")
      for x in data["verifydist"]:
        await ctx.send(x)
      data["verifydist"].clear()
      lists.setother(data)
      await ctx.send("Distro Verification Logs Cleared")

  @commands.Cog.listener()
  async def on_message(self,msg):
    condat=lists.readdataE()
    if int(msg.channel.id)==condat[str(msg.guild.id)]["distchan"]:
      cnt=msg.content
      pts=cnt.split("\n")
      #print(pts)
      u=pts[1]
      users=u.split(" ")
      l=pts[2]
      loot=l.split(";")
      purp=pts[0]
      data=lists.bals().copy()
      #print(type(data))
      prebal=data[str(msg.guild.id)]["clan"].copy()
      thrd=await msg.create_thread(name="Calculations (How Much Everyone Gets)")
      allow=[]
      block=[]
      lootItems=[]
      for x in loot:
        #print(x)
        if isinstance(x,str):
          lootItems.append(x)
      #print(lootItems)
      for x in lootItems:
          itemName=x.split(":")[0]
          #print(itemName)
          if itemName in lists.readother()["alloweditems"]:
            allow.append(x)
            #print("allow")
          else:
            #print("deny")
            block.append(x)
      #print(block)
      #print(allow)
      if len(block)==0:
        pass
      else:
        await thrd.send(f"Sorry The Following Items: {block} are not registered in my system and have NOT been counted for. Please see https://discord.com/channels/1031900634741473280/1145413798153437264 for the item name reference list.")
      for x in allow:
        try:
          #print(x)
          loc=allow.index(x)
          w=loot[loc].split(":")
          item=str(w[0])
          amount=int(w[1])
          #print(f'{item} : {amount}')
          percent=float(condat[str(msg.guild.id)]["clanPercent"]) #Percent The Clan Gets
          whole=amount
          if purp == "withdrawal":
            pw= whole
            div=round(pw)
          else:
            pw=percent*whole
            div=round(pw/100)
          cbala=0
          if amount > 0:
            cbala=data[str(msg.guild.id)]["clan"][str(item)]
            cbala=cbala+div
            await thrd.send(f"Clan Gets `{div}` `{item}`")
          else:
            cbala=0
            await thrd.send(f"Clan Gets Nothing From Withdrawls")
          if condat[str(msg.guild.id)]["storebal"].lower()=="no":
            cbala=data[str(msg.guild.id)]["clan"][str(item)]
            cbala=cbala+whole
            data[str(msg.guild.id)]["clan"][str(item)]=cbala
          else:
            cbala=data[str(msg.guild.id)]["clan"][str(item)]
            #print(f'Pre; {cbala}')
            cbala=cbala+div
            #print(f'Post: {cbala}')
            data[str(msg.guild.id)]["clan"][item]=cbala
          if purp=="withdrawal":
            rem=div
          else:
            rem=amount-abs(div)
          if condat[str(msg.guild.id)]["storebal"].lower()=="yes":
            #print("Storebal=yes")
            mem=round(rem/int(len(users)))
            memtot=mem*len(users)
            #print(memtot)
            #print(div+memtot)
            await thrd.send(f'The Listed Members Get `{mem}` `{item}` each.')
            #Code To Give The "Lost" Flux To The Clan
            if div+memtot != whole:
              dim=div+memtot
              missing=whole-dim
              cbalb=cbala+missing
              data[str(msg.guild.id)]["clan"][item]=cbalb
            for i in users:
              #print(i)
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
        except Exception as e:
          print(e)
      #print(2)
      other=lists.readother()
      endbal=data[str(msg.guild.id)]
      #print(1)
      lootdict={}
      for x in loot:
        p=list(x.split(":"))
        lootdict.update({str(p[0]):int(p[1])})
      #await thrd.send(prebal)
      #await thrd.send(endbal)
      sourceShip="{"+pts[3]+"}"
      destinationShip="{"+lists.readdataE()[str(msg.guild.id)]["distship"]+"}"
      date=pts[4].split("/")
      apit={"guildId":msg.guild.id,"channelId":msg.channel.id,"msgId":msg.id,"thrdId":thrd.id,"sourceShip":sourceShip,"destinationShip":destinationShip,"userClaim":lootdict,"purpose":purp,"date":date,"clanData":endbal}#prebal,endbal,msg.content,data[str(msg.guild.id)],lootdict,purp]
      #print(apit)
      other["verifydist"].append(apit)
      #print(other['verifydist'])
      if condat[str(msg.guild.id)]["verbal"]=="yes":
        lists.setother(other)
        await msg.add_reaction("⬆")
      else:
        dat=lists.readdata()
        dat=data
        lists.setdata(dat)
        await msg.add_reaction("⏫")
    else:
      pass

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

  @staticmethod
  async def verifyDistroLogsNew(self):
    print("Verifying Distro Logs")
    a=0
    data=lists.readdataE()
    oth=lists.readother()
    distdat=lists.readdata()
    dailyData=oth["verifydist"]
    print(dailyData)

    def findRelatingLogs(data, key, hex):
      return list(filter(lambda x: x.get(key) == hex, data))

    shipItemTotals={}
    claimedPerShip={}
    logsUsed={}
    ships=[]
    for log in dailyData:
      hex=log["sourceShip"]
      items=log["userClaim"]
      if hex not in list(claimedPerShip.keys()):
        claimedPerShip.update({hex:items})
      else:
        for item in list(items.keys()):
          oldTotal=claimedPerShip[item]
          newTotal=oldTotal+items[item]
          claimedPerShip[item]=newTotal
      ships.append(hex)
    for ship in ships:
      logsForShip=findRelatingLogs(dailyData,"sourceShip",ship)
      for message in logsForShip:
        result=True
        count=0
        guild=self.bot.get_guild(int(message["guildId"]))
        channel=guild.get_channel(int(message["channelId"]))
        mesg=await channel.fetch_message(int(message["msgId"]))
        thread=guild.get_thread(int(message["thrdId"]))
        date=f"{message['date'][2]}_{message['date'][0]}_{message['date'][1]}"
        logFile = f"https://pub.drednot.io/prod/econ/{date}/log.json.gz"
        shipFile = f"https://pub.drednot.io/prod/econ/{date}/ships.json.gz"
  
        log_response = requests.get(logFile)
        log_data = gzip.decompress(log_response.content)  #.decode('utf-8')
        logItems = loads(log_data)
        ships_response = requests.get(shipFile)
        shipsData = gzip.decompress(ships_response.content).decode('utf-8')
        ships= loads(shipsData)
        try:
          logList=findRelatingLogs(logItems,"src",message["sourceShip"])
          negativeList=findRelatingLogs(logItems,"dst",message["sourceShip"])
          positiveLogs=findRelatingLogs(positiveLogs,"dst",message["destinationShip"])
          withdrawals=findRelatingLogs(logItems,"src",message["sourceShip"])
          itemTotals={}
          for lootItem in list(message["userClaim"].keys()):
            itemId=int(lists.itemNameToID(lootItem))
            itemDeposits=findRelatingLogs(positiveLogs,"item",itemId)
            itemWithdrawals=findRelatingLogs(withdrawals,"item",itemId)
            netTotal=0
            for log in itemDeposits:
              netTotal+=log["count"]
            for log in itemWithdrawals:
              netTotal-=log["count"]
            shipItemTotals[hex][lootItem]+=netTotal
        except Exception as e:
          print(e)
          if hasattr(e, 'message'):
            emes=e.message
          else:
            emes=e
          print(emes)
          print(traceback.format_exc())
          await mesg.add_reaction("🤷")
          print("Error Occured")
        if result:
          await mesg.add_reaction("✅")
          distdat[str(mesg.guild.id)]=message["clanData"]
          lists.setdata(distdat)
        else:
          await mesg.add_reaction("❌")
        print("Reaction Added")
  #else:
    #pass
      oth["verifydist"].remove(message)
    others=lists.readother()
    others["verifydist"]=[]
    lists.setother(others)
    print("All Logs Verified")

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