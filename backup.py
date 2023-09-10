import os, discord
import time
import datetime
import pytz
#from keep_alive import keep_alive
from discord.ext import commands
from json import loads, dumps
from startup import startup

def backrel():
  with open('../NLDB/relations.json','r') as firstfile, open('Backups/rel2.json','w') as secondfile:
      
    # read content from first file
    for line in firstfile:
               
             # write content to second file
             secondfile.write(line)

def backdist():
  with open('../NLDB/distribution.json','r') as firstfile, open('Backups/distri2.json','w') as secondfile:
      
    # read content from first file
    for line in firstfile:
               
             # write content to second file
             secondfile.write(line)

def backqp():
  with open('../NLDB/quickping.json','r') as firstfile, open('Backups/qp2.json','w') as secondfile:
      
    # read content from first file
    for line in firstfile:
               
             # write content to second file
             secondfile.write(line)

def backdes():
  with open('../NLDB/designs.json','r') as firstfile, open('Backups/des2.json','w') as secondfile:
      
    # read content from first file
    for line in firstfile:
               
             # write content to second file
             secondfile.write(line)

def backoth():
  with open('../NLDB/other.json','r') as firstfile, open('Backups/oth2.json','w') as secondfile:
      
    # read content from first file
    for line in firstfile:
               
             # write content to second file
             secondfile.write(line)

def backconfig():
  with open('../NLDB/config.json','r') as firstfile, open('Backups/con2.json','w') as secondfile:
      
    # read content from first file
    for line in firstfile:
               
             # write content to second file
             secondfile.write(line)

def logback(ctx):
  tz = pytz.timezone('America/New_York')
  ct = datetime.datetime.now(tz)
  user = ctx.message.author.name
  data = user,ct
  print(data)
  with open("Backups/bcklog.txt", "a+") as g:
    g.write(f'Backed Up on {ct} by {user}')
    g.write('\n')

def backup(ctx):
  backrel()
  backdist()
  backdes()
  backqp()
  backoth()
  backconfig()
  #logback(ctx)
  #ct = datetime.datetime.now()
  #f = open(name, "w")