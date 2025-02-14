import os
import discord
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

def is_guild_owner():
  def predicate(ctx):
      return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id or ctx.author.id in lists.developers
  return commands.check(predicate)

def is_banned():
  def check_banned(ctx):
    return ctx.message.author.id not in banned
  return commands.check(check_banned)

def is_developer():
  def check_developer(ctx):
    return ctx.message.author.id in developers
  return commands.check(check_developer)

def is_authorized():
  def check_auth(ctx):
    gid = str(ctx.message.guild.id)
    uid = str(ctx.message.author.id)
    data = lists.readFile("config")[gid]["auth"]
    return (uid in data and uid not in banned) or (int(uid) in developers)
  return commands.check(check_auth)