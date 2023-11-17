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
    design=design.lower()
    if str(ctx.message.author.id) not in banned:
      gid = str(ctx.message.guild.id)
      data=lists.readdataD()
      if int(ctx.message.author.id) == data[gid][str(design)]["Designer"]:
        try:
          data[gid][design][item] = str(value)
          lists.setdataD(data)
          #lists.logback(ctx,msg)
          await ctx.send(f'Now {design} has a {value} value of {value}.')
        except KeyError:
          await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
      else:
        await ctx.send(f"You are not the Designer of {design} and cannot edit it.")
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
  
  @commands.command(name='adddes', brief="Adds A Design To The Ship Design Database", help="Adds a design to the ship design database. Args: <ShipName (NO SPACES)> {Design Image (First and Only Attachment)}")
  async def savedesigns(self,ctx,*,design):
    msg="a b"
    design=design.lower()
    if str(ctx.message.author.id) not in banned:
      try:
        gid = str(ctx.message.guild.id)
        msgparts, data = msg.split(" "), lists.readdataD()
        auth = ctx.message.author.id
        try:
          img = ctx.message.attachments[0]
          img2 = img.url
        except:
          img=None
          img2=None
        #print(img2)
        default = {"Designer":int(auth),"Image":None}
        data[gid].update({design:default})
        #print(data)
        lists.setdataD(data)
        #lists.logback(ctx,design)
        await ctx.send(f'Added {design} to the Database')
      except KeyError as e:
        print(e)
        await ctx.send(f'KeyError: The command had a KeyError, due to the complexity of this command the value causing the error cannot be given.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
  
  @commands.command(name='deldes', brief="Deletes A Design From The Ship Design Database", help="Deletes a ship from the ship design database. Args: <ShipName>")
  async def deldes(self,ctx, *, design):
    data = lists.readdataD()
    gid = str(ctx.message.guild.id)
    design=design.lower()
    if str(ctx.message.author.id) not in banned:
      if int(ctx.message.author.id) == data[gid][str(design)]["Designer"]:
        try:
          del data[gid][design]
          lists.setdataD(data)
          #lists.logback(ctx,design)
          await ctx.send(f'Deleted {design} from the Database')
        except KeyError:
          await ctx.send(f'KeyError! {design} does not exist in my database! Please use n!design all if you would like to call all designs or n!design list for a list of design names.')
      else:
        await ctx.send(f'You are not the Designer of {design} and cannot delete it')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')
  
  @commands.command(name='design', brief="Calls A Design From The Ship Design Database", help="Calls a design from the database. Input a ship name, or all to get one or all the ships in the database. n!design all calls all designs. n!design list lists all design names.")
  async def calldes(self,ctx,*,design):
    if str(ctx.message.author.id) not in banned:
      try:
        design=str(design.lower())
        print(design)
        if design=="list designs":
          gid = str(ctx.message.guild.id)
          data=lists.readdataD()
          k=discord.Embed(title="Design List")
          for x in data[gid]:
            k.add_field(name="Design Name",value=x)
            k.add_field(name="Designer",value=f'<@{int(data[x]["Designer"])}>')
          await ctx.send(embed=k)
        else:
          gid = str(ctx.message.guild.id)
          data=lists.readdataD()
          #lists.logback(ctx,design)
          e = discord.Embed(title=design)
          e.set_image(url=str(data[gid][design]["Image"]))
          e.add_field(name="Designer",value=f'<@{data[gid][design]["Designer"]}>',inline=True)
          keylist=list(data[gid][design].keys())
          keylist.remove("Designer")
          keylist.remove("Image")
          for key in keylist:
            e.add_field(name=str(key),value=data[gid][design][str(key)],inline=True)
        #tz = pytz.timezone('America/New_York')
          await ctx.send(embed=e)
      except KeyError:
        await ctx.send(f'KeyError! {design} does not exist in my database! Please use n!design all if you would like to call all designs or n!design list for a list of design names.')
    else:
      await ctx.send('Your ID is in the Banned List, you are not allowed to use New Light. If you belive this to be an error please DM JaWarrior#6752')

async def setup(bot: commands.Bot):
    await bot.add_cog(DesCmds(bot))