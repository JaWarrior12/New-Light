import time
import pytz
import datetime
import os, discord
import asyncio
from discord.ext import commands

async def startup():
  #await asyncio.sleep(5)
  print("Starting Back Up")
  os.system('py main.py')

def logdown():
  tz = pytz.timezone('America/New_York')
  ct = datetime.datetime.now(tz)
  print("Disconnected")
  #print(data)
  with open("Backups/disconnectlogs.txt", "a+") as o:
    o.write('\n')
    o.write(f'New Light disconnected from the DISCORD platform at {ct}.')
    o.write('\n')