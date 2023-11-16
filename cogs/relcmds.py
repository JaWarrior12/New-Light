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

class RelCmds(commands.Cog, name="Relations Commands",description="Clan Relations Commands"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name='rel',brief="Gets a clan's relation.",help="Calls a relation from a clan's relation database. Format: n!rel clan; Clan can be a clan's name, emoji, or abbreviation.")
  async def relations(self,ctx, *, clan):
        #lists.logback(ctx,clan)
        if str(ctx.message.author.id) not in banned:
          try:
            st=None
            if len(clan) >= 5:
              st="name"
            elif len(clan) == 1:
              st="emoji"
            elif len(clan) <= 4:
              st="abrv"
            else:
              st="name"
            datab = lists.readdataB()[str(ctx.message.guild.id)]
            def find_route(data, route_no):
              return list(filter(lambda x:x.get(st)==clan,datab))
            route = find_route(datab,clan)
            e=discord.Embed(title="Clan Relations")
            e.add_field(name="Clan Name",value=route[0]["name"],inline=True)
            e.add_field(name="Clan Abbreviation",value=route[0]["abrv"],inline=True)
            e.add_field(name="Clan Emoji",value=route[0]["emoji"],inline=True)
            e.add_field(name="Relation",value=route[0]["relation"],inline=True)
            await ctx.send(embed=e)
          except:
            await ctx.send(f'Error: {clan} is not in the relations database. Either {clan} has not been entered into the list by a clan leader or it is listed under a different key.')
        else:
          await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
          return False
         
  @commands.command(name="changerel",brief="Changes clan relations. (LR)",help="Changes a clan's relation in their relations database. Format: n!changerel relation clan; Clan can be the emoji, name, or abreviation")
  async def changerel(self,ctx, relation,*, clan):
      if str(ctx.message.author.id) not in banned:
        msg="a b"
        msgparts, data = msg.split(" "), lists.readdataB()
        msgb = str(clan+" "+relation)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        #lists.logback(ctx,msgb)
        if chk == True:
          try:
            #data[gid][clan]=str(relation)
            #lists.setdataB(data)
            #await ctx.send(f'Now {clan} has a relation of {relation} in {ctx.message.guild.name}')
            st=None
            if len(clan) >= 5:
              st="name"
            elif len(clan) == 1:
              st="emoji"
            elif len(clan) <= 4:
              st="abrv"
            else:
              st="name"
            datab = lists.readdataB()[str(ctx.message.guild.id)]
            datac=lists.readdataB()
            def find_route(data, route_no):
              return list(filter(lambda x:x.get(st)==clan,datab))
            route = find_route(datab,clan)
            datab.index(route[0])
            datab.copy()
            #datab.count(clan)
            #await ctx.send(datab.count(clan))
            #await ctx.send(route)
            datab[datab.index(route[0])]['relation']=relation
            datac[str(ctx.message.guild.id)][datab.index(route[0])]['relation']=relation
            #await ctx.send(datab)
            #await ctx.send(datac)
            lists.setdataB(datac)
            e=discord.Embed(title="Clan Relation Changed")
            e.add_field(name="Changed By",value=ctx.message.author.display_name,inline=True)
            e.add_field(name="Clan Name",value=datac[str(ctx.message.guild.id)][datab.index(route[0])]['name'],inline=True)
            e.add_field(name="Clan Abbreviation",value=datac[str(ctx.message.guild.id)][datab.index(route[0])]['abrv'],inline=True)
            e.add_field(name="Clan Emoji",value=datac[str(ctx.message.guild.id)][datab.index(route[0])]['emoji'],inline=True)
            e.add_field(name="Relation",value=datac[str(ctx.message.guild.id)][datab.index(route[0])]['relation'],inline=True)
            #e.timestamp=datetime.now()
            await ctx.send(embed=e)
          except KeyError:
            await ctx.send(f'KeyError: {clan} Is not in the relations database. Either {clan} has not been entered into the list by a clan leader or it is listed under a different key. Fixes: Capitalize the first letter (cougar -> Cougar), Use an abbreviation (Swiss Armed Forces -> SAF), or remove spaces in the name (Hellenic League -> HellenicLeague). The solution could be a mix of the provided fixes.')
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")
      else:
          await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
          return False
          
  
  @commands.command(name="addrel",brief="Adds a clan to relations (LR)",help="Adds a relation to a clan's relation database. Format: n!addrel relation emoji clan_abbreviation clan_full_name; \n-The abbreviation must be 4 letters or less, the full name can have spaces.")
  async def addrel(self,ctx,relation=None,emoji=None,abrv=None,*,full_name=None):
        msg="a b"
        #msgparts, data = msg.split(" "), lists.readdataB()
        msgb = str(emoji+" "+relation+" "+abrv+" "+full_name)
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        #lists.logback(ctx,msgb)
        if chk == True:
          try:
            #data[gid][clan]=str(relation)
            #lists.setdataB(data)
            #await ctx.send(f'Now {full_name} has a relation of {relation} in {ctx.message.guild.name}')
            data=lists.readdataB()
            newcon=[{'name':str(full_name),'emoji':emoji,'abrv':str(abrv),'relation':str(relation)}]
            data[str(ctx.message.guild.id)].extend(newcon)
            lists.setdataB(data)
            e=discord.Embed(title="Clan Relation Added")
            e.add_field(name="Clan Name",value=full_name,inline=True)
            e.add_field(name="Clan Abbreviation",value=abrv,inline=True)
            e.add_field(name="Clan Emoji",value=emoji,inline=True)
            e.add_field(name="Relation",value=relation,inline=True)
            #e.timestamp=datetime.now()
            await ctx.send(embed=e)
          except KeyError:
            await ctx.send(f'KeyError: {full_name} Is not in the relations database. Either {full_name} has not been entered into the list by a clan leader or it is listed under a different key. Fixes: Capitalize the first letter (cougar -> Cougar), Use an abbreviation (Swiss Armed Forces -> SAF), or remove spaces in the name (Hellenic League -> HellenicLeague). The solution could be a mix of the provided fixes.')
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")

  @commands.command(name='delrel',brief="Gets a clan's relation.",help="Calls a relation from a clan's relation database. Format: n!rel clan; Clan can be a clan's name, emoji, or abbreviation.")
  async def delrel(self,ctx, *, clan):
        #lists.logback(ctx,clan)
        if str(ctx.message.author.id) not in banned:
          try:
            st=None
            if len(clan) >= 5:
              st="name"
            elif len(clan) == 1:
              st="emoji"
            elif len(clan) <= 4:
              st="abrv"
            else:
              st="name"
            dataA=lists.readdataB()
            datab = dataA[str(ctx.message.guild.id)]
            def find_route(data, route_no):
              return list(filter(lambda x:x.get(st)==clan,datab))
            route = find_route(datab,clan)
            e=discord.Embed(title="Clan Relations Updated :: Clan Deleted")
            e.add_field(name="Clan Name",value=route[0]["name"],inline=True)
            e.add_field(name="Clan Abbreviation",value=route[0]["abrv"],inline=True)
            e.add_field(name="Clan Emoji",value=route[0]["emoji"],inline=True)
            e.add_field(name="Relation",value=route[0]["relation"],inline=True)
            await ctx.send(embed=e)
            dataA[str(ctx.message.guild.id)].remove(route[0])
            lists.setdataB(dataA)
          except:
            await ctx.send(f'Error: {clan} is not in the relations database. Either {clan} has not been entered into the list by a clan leader or it is listed under a different key.')
        else:
          await ctx.send('Your ID Is In The Banned List and you cannot use New Light. If you think this is an error please contact JaWarrior#6752.')
          return False
  
  @commands.command(name='relall',brief="Fetches the server's complete relations list. (LR)",help="Calls all of a clan's relations in their relations database. Format: n!relall")
  async def relall(self,ctx,*,clan=None):
        #msgparts, data = msg.split(" "), lists.readdataB()
        chk = lists.checkperms(ctx)
        gid = str(ctx.message.guild.id)
        #lists.logback(ctx,clan)
        mesg = str(gid)
        if chk == True:
          await ctx.send('List of All Relations')
          await ctx.send(dumps(lists.readdataB()[mesg]).replace(': "',' = ').replace('{','').replace(',','\n').replace('}','').replace('"',''))
        else:
          await ctx.send(f"You are not authorized to use leadership commands in {ctx.guild.name}")

  @commands.command(name="reltest",hidden=True,disabled=True)
  @commands.has_role("Developer")
  async def reltest(self,ctx,*,clan):
    if int(ctx.message.author.id) in lists.developers:
      st=None
      if len(clan) >= 5:
        st="name"
      elif len(clan) == 1:
        st="emoji"
      elif len(clan) <= 4:
        st="abrv"
      else:
        st="name"
      datab = lists.readdataB()[str(ctx.message.guild.id)]
      def find_route(data, route_no):
        return list(filter(lambda x:x.get(st)==clan,datab))
      route = find_route(datab,clan)
      e=discord.Embed(title="Clan Relations")
      e.add_field(name="Clan Name",value=route["name"],inline=True)
      e.add_field(name="Clan Abbreviation",value=route["abrv"],inline=True)
      e.add_field(name="Clan Emoji",value=route["emoji"],inline=True)
      e.add_field(name="Relation",value=route["relation"],inline=True)
      await ctx.send(embed=e)
    else:
      await ctx.send("This is a developer only command.")

async def setup(bot: commands.Bot):
    await bot.add_cog(RelCmds(bot))