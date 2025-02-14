import os
import discord
from os import system
import time
import pytz
from datetime import datetime, timezone
from discord.ext import commands
from discord.utils import get
from discord import Member
from discord import app_commands
from discord.ext.commands import has_permissions, MissingPermissions
from json import loads, dumps
import requests

#Lists
import lists

banned = lists.banned
developers = lists.developers

bots=0

class OtherCmds(commands.Cog, name="Other Commands",description="Extra Commands + Pingpage + Wiki Link + Setup Guide"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    global bots
    bots=self.bot

  @commands.command(name='ping',brief="Latency Command",help="Latency Command")
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def ping(self,ctx):
    await ctx.send(f"Pong 🏓! Latency: {round(int(self.bot.latency)*1000)}ms")

  @commands.command(name='test',brief='Test Command for devs.',hidden=True)
  #@commands.has_role('Developer')
  async def test(self,ctx):
    lists.logdown()
    await ctx.send("hi")

  @commands.command(name="wiki",help="Link To Github Wiki")
  async def wiki(self,ctx):
    await ctx.send("Wiki: https://github.com/JaWarrior12/New-Light/wiki")


  @commands.command(name="invitehelp",help="This command DMs you information on inviting New Light to your server. Format: n!invitehelp @Yourself",disabled=False,hidden=False)
  async def invitehelp(self,ctx):
    await ctx.send("Setup Guide: https://github.com/JaWarrior12/New-Light/wiki/Setup-Guide")

  @commands.command(name="pingpage",aliases=["pinger","ppage","p"],brief="Link to WebPing Page",help="Sends the link to New Light Remote WebPing Page",disabled=True,hidden=True)
  async def pingpage(self,ctx):
    await ctx.send("New Light Ping Page: https://new-light-discord-bot.jawarrior.repl.co")

  @commands.command(name="whois",help="Gets Clans A Member Is In",hidden=True,disabled=True)
  async def whois(self,ctx,member:discord.Member):
    shargids=member.mutual_guilds
    e=discord.Embed(title=f"Servers {member.name} Shares With New Light")
    e.set_thumbnail(url=member.display_avatar)
    for x in shargids:
      e.add_field(name=x,value=member.dispaly_name,inline=True)
      pass
    await ctx.send(embed=e)

  @commands.command(name="event",help="Calls The Swiss Army Event Timer",disabled=True,hidden=True)
  async def saftimer(self,ctx):
    r = requests.get("link here")
    tdat=r.json()
    e=discord.Embed(title=f"Swiss Army Event Timer")
    e.add_field(name="",value=tdat["us"],inline=False)
    e.add_field(name="",value=tdat["eu"],inline=False)
    e.add_field(name="",value=tdat["asia"],inline=False)
    await ctx.send(embed=e)

async def setup(bot: commands.Bot):
  await bot.add_cog(OtherCmds(bot))


  