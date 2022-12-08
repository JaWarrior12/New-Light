import unittest
from main import *

import lists
import relations.json
import os, discord
import time
import pytz
import datetime 
from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup

class UnitTests(unittest.TestCase):

  def test_relations(self):
      clan="HL"
      relation="Enemy"
      gid="1031900634741473280"
      st=None
      if len(clan) >= 5:
        st="name"
      elif len(clan) == 1:
        st="emoji"
      elif len(clan) <= 4:
        st="abrv"
      else:
        st="name"
      datab = lists.readdataB()[gid]
      datac=lists.readdataB()
      def find_route(data, route_no):
        return list(filter(lambda x:x.get(st)==clan,datab))
        route = find_route(datab,clan)
        datab.index(route)
        datab.copy()
        #datab.count(clan)
        #await ctx.send(datab.count(clan))
        #await ctx.send(route)
        datab[datab.index(route)]['relation']=relation
        datac[gid][route]['relation']=relation
        #await ctx.send(datab)
        print(datab)
        print(datac)
        #await ctx.send(datac)
        lists.setdataB(datac)
    

