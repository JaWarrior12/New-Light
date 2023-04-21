import os, discord
import time
import pytz
import datetime 
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

class DesCmds(commands.Cog, name="Ship Design Database Commands",description="Ship Design Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name='editdes', brief="Edits A Design In The Ship Design Database",help="Edits A Design In The Ship Design Database. Args: <ShipName (NO SPACES)> <DataPoint> <NewValue>")
  async def fetchdesign(self,ctx, design,item,value):
    msg="a b"
    if str(ctx.message.author.id) not in banned:
      gid = str(ctx.message.guild.id)
      msgparts, data = msg.split(" "), lists.readdataD()
      try:
        data[gid][design][item] = str(value)
        lists.setdataD(data)
        lists.logback(ctx,msg)
        await ctx.send(f'Now {design} has a {value} value of {value}.')
      except KeyError:
        await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
  
  @commands.command(name='adddes', brief="Adds A Design To The Ship Design Database", help="Adds a design to the ship design database. Args: <ShipName (NO SPACES)> {Design Image (First and Only Attachment)}")
  async def savedesigns(self,ctx,public="no",*,design):
    msg="a b"
    if str(ctx.message.author.id) not in banned:
      try:
        gid = str(ctx.message.guild.id)
        msgparts, data = msg.split(" "), lists.readdataD()
        auth = ctx.message.author.id
        auth2 = f'<@{auth}>'
        img = ctx.message.attachments[0]
        img2 = img.url
        #print(img2)
        default = {"Designer":auth2,"Image":img2,"Public?":public}
        data[gid][design]=dict(default)
        #print(data)
        lists.setdataD(data)
        lists.logback(ctx,design)
        await ctx.send(f'Added {design} to the Database')
      except KeyError:
        await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
  
  @commands.command(name='deldes', brief="Deletes A Design From The Ship Design Database", help="Deletes a ship from the ship design database. Args: <ShipName>")
  async def deldes(self,ctx, *, design):
    msg="a b"
    if str(ctx.message.author.id) not in banned:
      try:
        gid = str(ctx.message.guild.id)
        msgparts, data = msg.split(" "), lists.readdataD()
        data = lists.readdataD()
        del data[gid][design]
        lists.setdataD(data)
        lists.logback(ctx,design)
        await ctx.send(f'Deleted {design} from the Database')
      except KeyError:
        await ctx.send(f'KeyError: The Key {design} is not found in the database. There might have been an error entering the key. Fixes: Capitialization (bruh -> Bruh), Spaces (Pls Join -> PlsJoin), Abbreviation (Distribution -> Distri). The solution to this error may be a mix of the 3 fixes provided.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
  
  @commands.command(name='calldes', brief="Calls A Design From The Ship Design Database", help="Calls a design from the database. Input a ship name, or all to get one or all the ships in the database.")
  async def calldes(self,ctx,*,design):
    msg="a b"
    if str(ctx.message.author.id) not in banned:
      try:
        gid = str(ctx.message.guild.id)
        msgparts, data = msg.split(" "), lists.readdataD()
        data2 = msg.split(" ")
      #data[msgparts[0]][msgparts[1]] = str(msgparts[2])
      #data2[msgparts[0]][msgparts[1]]
      #p1 = msgparts[0]
        a = "all"
        b = "specific"
        lists.logback(ctx,design)
        #c = "categorysize"
        if design == a:
          await ctx.send(dumps(lists.readdataD()[gid]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n'))
      #elif msgparts[0] == b:
       # await ctx.send(dumps(readdataD()[data]).replace(':', '=').replace('{', '').replace('}', '').replace('"', ''))
        else: #design== b:
          await ctx.send(dumps(lists.readdataD()[gid][str(design)]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n'))
      #elif msgparts[0] == c:
       # await ctx.send(dumps(readdataD())).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n')
      except KeyError:
        await ctx.send(f'KeyError: The Key {design} is not found in the database. There might have been an error entering the key. Fixes: Capitialization (bruh -> Bruh), Spaces (Pls Join -> PlsJoin), Abbreviation (Distribution -> Distri). The solution to this error may be a mix of the 3 fixes provided.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

  @calldes.error
  async def calldes_error(self, ctx, error):
      if isinstance(error, commands.CheckFailure):
        await ctx.send('Your input does not match any command, for n!calldes please use n!calldes <shipname> or n!calldes all to call specific design groups.')

async def setup(bot: commands.Bot):
    await bot.add_cog(DesCmds(bot))