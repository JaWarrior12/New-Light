import os, discord
from os import system
import time
import pytz
import datetime 
from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
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

class OtherCmds(commands.Cog, name="Other Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name='test',brief='Test Command for devs.',hidden=True)
  @commands.has_role('Developer')
  async def test(self,ctx):
    lists.logdown()
    await ctx.send("hi")

  @commands.command(name="listtest",hidden=True)
  @commands.has_role('Developer')
  async def listtesting(self,ctx):
    if ctx.message.author.id in developers:
      key = "lt"
      mylist = []
      data = dumps(lists.readother()['lt']).replace("[","").replace("]","").replace(' ',"").replace("'","").replace('"',"")
      print(data)
      mylist = list(data)
      await ctx.send(mylist)
      key=","
      for x in mylist:
        print(x)
        if x == ",":
          mylist.remove(x)
          await ctx.send(f'Removed {x}')
          await ctx.send(mylist)
          continue
      await ctx.send(mylist)
      await ctx.send(type(mylist))
      await ctx.send(mylist)

  @commands.command(name="chl",hidden=True)
  @commands.has_role('Developer')
  async def chlist(self,ctx,msg):
    if ctx.message.author.id in developers:
      key = "lt"
      keyb = str("auth")
      gid = str(ctx.message.guild.id)
      mylist = []
      msgb = "a b"
      msgparts, data = msgb.split(" ")
      datab = dumps(lists.readdataE()[gid][keyb]).replace("[","").replace("]","").replace('"',"").replace("'","")
      await ctx.send(datab)
      await ctx.send("-----")
      await ctx.send(type(datab))
      mylist = list(datab)
      await ctx.send(mylist)
      key=","
      for x in mylist:
        print(x)
        if x == ",":
          mylist.remove(x)
          await ctx.send(f'Removed {x}')
          await ctx.send(mylist)
          continue
      await ctx.send(mylist)
      await ctx.send(type(mylist))
      await ctx.send(mylist)
      mylist.append(msg)
      await ctx.send(mylist)
      data[gid][keyb]=mylist
      await ctx.send(data)
      lists.setdataE(data)
      
    else:
      await ctx.send("You are not a developer and cannot use this command")

  @commands.command(name="invitehelp",help="This command DMs you information on inviting New Light to your server. Format: n!invitehelp @Yourself")
  async def invitehelp(self,ctx,user:discord.User):
    with open('InviteHelp.txt', 'rb') as fp:
        await user.send(file=discord.File(fp, 'New Light Documentation'))
    f = open("InviteHelp.txt", "r")
    if f.mode == 'r':
      contents = f.read()
      await user.send("Invite Help Documentation")

  @commands.Cog.listener()
  async def on_disconnect():
    try:
      lists.logdown()
    except KeyError as e:
      print(e.args[0])
      lists.logdown()


  @commands.command(name="authuser",help="Authorizes A User To Use Leadership Commands. Required Permissions: Administrator; Format: n!authuser <USERID>")
  @commands.has_permissions(administrator=True)
  async def authorizeuser(self,ctx,user):
    if str(ctx.message.author.id) not in banned:
      chk = lists.checkperms(ctx)
      if chk == True:
        #await lists.logmajor(ctx,user)
        lists.logback(self,ctx,user)
        gid=str(ctx.message.guild.id)
        key="auth"
        data = dumps(lists.readdataE()[gid][key])
        if str(user) in data:
          await ctx.send(f'The User With An ID Of {user} Is Already Authorized')
        else:
          print(data)
          ##await ctx.send("----")
          #await ctx.send(data)
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
          datab[gid][key]=use
          lists.setdataE(datab)
          await ctx.send(f'The User With A User Id Of {user} has been authorized to use Leadership Commands in the server {ctx.message.guild.name} by {ctx.message.author.name}')
      else:
        await ctx.send("You are not authorized and CANNOT authorize users.")
    elif str(ctx.messsage.author.id) in banned:
      await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
    

def setup(bot: commands.Bot):
    bot.add_cog(OtherCmds(bot))