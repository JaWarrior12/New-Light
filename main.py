import os, discord
from keep_alive import keep_alive
from discord.ext import commands
from json import loads, dumps

authorized = [949451462151376948, 722703947638505556, 832250002562220062, 445763770799620097, 907899780561272842]
bot = commands.Bot(command_prefix='n!')

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
      channel = self.get_destination()
      with open('Documentation.txt', 'rb') as fp:
        await channel.send(file=discord.File(fp, 'Documentation'))
        #f = open("Documentation.txt", "r")
        #if f.mode == 'r':
        #    contents = f.read()
        #    await channel.send("New Light Documentation")
        #    await channel.send(contents)


bot.help_command = MyHelp()

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    activity = discord.Game(name="JaWarrior.py & n!help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

#Server IDs
NLC = 75778020639932516
SCP = 966067610779271168
TestSrvr = 975858783504969808

def readdata():
    return loads(open('distribution.json', 'r').read())


def setdata(data):
    with open("distribution.json", "w") as f:
        f.write(dumps(data))


def readdataB():
    return loads(open("relations.json","r").read())


def setdataB(dataB):
    with open("relations.json", "w") as g:
        g.write(dumps(dataB))

def readdataC():
    return loads(open('quickping.json', 'r').read())

def readdataD():
    return loads(open('designs.json', 'r').read())

def setdataD(dataD):
    with open("designs.json", "w") as g:
        g.write(dumps(dataD))

def getguild(ctx):
  id = ctx.message.guild.id
  print(id)
  return id

@bot.command(name="logloot")
async def returnpaymentdata(ctx, *, msg):
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "SCP"
      c = "TestServer"
      if getguild(ctx) == NLC:
        if msgparts[0] == a:
          data[msgparts[0]][msgparts[1]][msgparts[2]] = int(msgparts[3])
          setdata(data)
          await ctx.send(f'now {msgparts[0]} has {msgparts[2]} {msgparts[1]}')
        else:
         await ctx.send('Error! Please use n!logloot NLC "username" "item" "new value"! You can only run NLC update commands in the NLC server')
      elif getguild(ctx) == SCP:
        if msgparts[0] == b:
          print(1)
          data[msgparts[0]][msgparts[1]][msgparts[2]] = int(msgparts[3])
          setdata(data)
          await ctx.send(f'now {msgparts[0]} has {msgparts[2]} {msgparts[1]}')
        else:
         await ctx.send('Error! Please use n!logloot SCP "username" "item" "new value"! You can only run SCP update commands in the SCP server!')
      elif getguild(ctx) == TestSrvr:
        print(2)
        if msgparts[0] == c:
          data[msgparts[0]][msgparts[1]][msgparts[2]] = int(msgparts[3])
          setdata(data)
          await ctx.send(f'now {msgparts[0]} has {msgparts[2]} {msgparts[1]}')
        else:
          await ctx.send('Error! Please use n!logloot TestServer "username" "item" "new value"! You can only run TestServer update commands in the TestServer server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    else:
        await ctx.send('Unapproved Operator.')


@bot.command(name='reset')
async def resetalldata(ctx, *, msg):
  if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "SCP"
      c = "TestServer"
      mesg = data[msgparts[0]][msgparts[1]]=str(msgparts[2])
      if getguild(ctx) == NLC:
        if msgparts[0] == a:
          print(1)
          data = readdata()
          for i in data[mesg].keys():
            data[mesg][i] = 0
          setdata(data)
          await ctx.send('User Data Reset')
        else:
          await ctx.send('Error! Please use n!logloot NLC "username" "item" "new value"! You can only run NLC update commands in the NLC server')
      elif getguild(ctx) == SCP:
        if msgparts[0] == b:
          print(2)
          data = readdata()
          for i in data[mesg].keys():
            data[mesg][i] = 0
          setdata(data)
          await ctx.send('User Data Reset')
        else:
         await ctx.send('Error! Please use n!logloot SCP "username" "item" "new value"! You can only run SCP update commands in the SCP server!')
      elif getguild(ctx) == TestSrvr:
        if msgparts[0] == c:
          print(3)
          data = readdata()
          for i in data[mesg].keys():
            data[mesg][i] = 0
          setdata(data)
          await ctx.send('User Data Reset')
        else:
          await ctx.send('Error! Please use n!logloot TestServer "username" "item" "new value"! You can only run TestServer update commands in the TestServer server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
  else:
    await ctx.send('Unapproved Operator.')

@bot.command(name='balance')
async def getuserloot(ctx, *, msg):
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "SCP"
      c = "TestServer"
      mesg = data[msgparts[0]]=str(msgparts[1])
      if getguild(ctx) == NLC:
        if msgparts[0] == a:
          print(1)
          await ctx.send(dumps(readdata()[mesg]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        else:
         await ctx.send('Error! Please use n!balance NLC "username"! You can only run NLC commands in the NLC server')
      elif getguild(ctx) == SCP:
        if msgparts[0] == b:
          print(2)
          await ctx.send(dumps(readdata()[mesg]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        else:
         await ctx.send('Error! Please use n!balance SCP "username"! You can only run SCP commands in the SCP server!')
      elif getguild(ctx) == TestSrvr:
        print(3)
        if msgparts[0] == c:
          await ctx.send(dumps(readdata()[mesg]).replace(':','=').replace('{','').replace('}','').replace('"',''))
        else:
          await ctx.send('Error! Please use n!balance TestServer "username"! You can only run TestServer commands in the TestServer server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')


@bot.command(name='rel')
async def relations(ctx, *, msg):
      msgparts, data = msg.split(" "), readdataB()
      a = "NLC"
      b = "SCP"
      c = "TestServer"
      mesg = data[msgparts[0]]=str(msgparts[1])
      if getguild(ctx) == NLC:
        if msgparts[0] == a:
          print(1)
          await ctx.send(dumps(readdataB()[mesg]).replace(':', '=').replace('{', '').replace('}', '').replace('"', ''))
        else:
          await ctx.send('Error! Please use n!logloot NLC "username" "item" "new value"! You can only run NLC update commands in the NLC server')
      elif getguild(ctx) == SCP:
        if msgparts[0] == b:
          print(2)
          await ctx.send(dumps(readdataB()[mesg]).replace(':', '=').replace('{', '').replace(
            '}', '').replace('"', ''))
        else:
         await ctx.send('Error! Please use n!logloot SCP "username" "item" "new value"! You can only run SCP update commands in the SCP server!')
      elif getguild(ctx) == TestSrvr:
        if msgparts[0] == c:
          print(3)
          await ctx.send(dumps(readdataB()[mesg]).replace(':', '=').replace('{', '').replace(
            '}', '').replace('"', ''))
        else:
          await ctx.send('Error! Please use n!logloot TestServer "username" "item" "new value"! You can only run TestServer update commands in the TestServer server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')

@bot.command(name='qp')
@commands.has_role('QuickPing')
async def quickping(ctx, *, msg):
  await ctx.send(dumps(readdataC()[msg]).replace('{','').replace('}', '').replace('"', ''))


@quickping.error
async def quickping_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Error, Required Role: QuickPing, Not Found')

@bot.command(name='balall')
async def balanceall(ctx,*,msg):
  if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdata()
      a = "NLC"
      b = "SCP"
      c = "TestServer"
      mesg = str(msgparts[0])
      if getguild(ctx) == NLC:
        if msgparts[0] == a:
          print(1)
          await ctx.send('Balances Of All Members')
          await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
        else:
          await ctx.send('Error! Please use n!balall NLC! You can only run NLC update commands in the NLC server')
      elif getguild(ctx) == SCP:
        if msgparts[0] == b:
          print(2)
          await ctx.send('Balances Of All Members')
          await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
        else:
         await ctx.send('Error! Please use n!balall SCP! You can only run SCP update commands in the SCP server!')
      elif getguild(ctx) == TestSrvr:
        if msgparts[0] == c:
          print(3)
          await ctx.send('Balances Of All Members')
          await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
        else:
          await ctx.send('Error! Please use n!balall TestServer! You can only run TestServer update commands in the TestServer server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
    #await ctx.send(  dumps(readdata()).replace(':','=').replace('{','').replace('}','').replace('"',''))
    #await ctx.send('Balances Of All Members')
    #await ctx.send(dumps(readdata()[mesg]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
  else:
     await ctx.send('Unapproved Operator.')

@bot.command(name="changerel")
async def changerel(ctx, *, msg):
    if ctx.message.author.id in authorized:
      msgparts, data = msg.split(" "), readdataB()
      data[msgparts[0]][msgparts[1]] = str(msgparts[2])
      a = "NLC"
      b = "SCP"
      c = "TestServer"
      mesg = data.str(msgparts[0])
      if getguild(ctx) == NLC:
        if msgparts[0] == a:
          print(1)
          setdataB(data)
          await ctx.send(f'now {msgparts[1]} has a relation of {msgparts[2]} in the clan {msgparts[0]}')
        else:
          await ctx.send('Error! Please use n!changerel NLC "Clan" "New Rel"! You can only run NLC update commands in the NLC server')
      elif getguild(ctx) == SCP:
        if msgparts[0] == b:
          print(2)
          setdataB(data)
          await ctx.send(f'now {msgparts[1]} has a relation of {msgparts[2]} in the clan {msgparts[0]}')
        else:
         await ctx.send('Error! Please use n!changerel SCP "Clan" "New Rel"! You can only run SCP update commands in the SCP server!')
      elif getguild(ctx) == TestSrvr:
        if msgparts[0] == c:
          print(3)
          setdataB(data)
          await ctx.send(f'now {msgparts[1]} has a relation of {msgparts[2]} in the clan {msgparts[0]}')
        else:
          await ctx.send('Error! Please use n!changerel TestServer "Clan" "New Rel"! You can only run TestServer update commands in the TestServer server!')
      else:
          await ctx.send('Error! Server Not In Approved List For This Command! If You Believe This Is An Error Please DM JaWarrior#6752.')
          setdataB(data)
          await ctx.send(f'now {msgparts[0]} has a relation of {msgparts[1]}')
    else:
        await ctx.send('Unapproved Operator.')

@bot.command(name='eddes')
@commands.has_role('Developer')
async def fetchdesign(ctx, *, msg):
  msgparts, data = msg.split(" "), readdataD()
  data[msgparts[0]][msgparts[1]] = str(msgparts[2])
  setdataD(data)
  await ctx.send(f'Now {msgparts[0]} has a {msgparts[1]} of {msgparts[2]}.')

@bot.command(name='addes')
@commands.has_role('Developer')
async def savedesigns(ctx, *, msg):
  msgparts, data = msg.split(" "), readdataD()
  data[msgparts[0]][msgparts[1]] = str(msgparts[2])
  #adds value data[msgparts[0]][msgparts[2]]=str(msgparts[1])
  setdataD(data)
  await ctx.send(f'Added {msgparts[2]} to size {msgparts[1]} of type {msgparts[0]}')

@bot.command(name='calldes')
async def calldes(ctx,*,msg):
  msgparts, data = msg.split(" "), readdataD()
  data2 = msg.split(" ")
  #data[msgparts[0]][msgparts[1]] = str(msgparts[2])
  #data2[msgparts[0]][msgparts[1]]
  #p1 = msgparts[0]
  a = "all"
  b = "category"
  #c = "categorysize"
  if msg == a:
    await ctx.send(dumps(readdataD()).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n'))
  #elif msgparts[0] == b:
   # await ctx.send(dumps(readdataD()[data]).replace(':', '=').replace('{', '').replace('}', '').replace('"', ''))
  elif msgparts[0] == b:
    await ctx.send(dumps(readdataD()[msgparts[1]]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n'))
  #elif msgparts[0] == c:
   # await ctx.send(dumps(readdataD())).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n')
  else:
    await ctx.send('Your input does not match any command, for n!calldes please use n!calldes category "category" or n!calldes all to call specific design groups.')

#@bot.command(name='getid')
#@commands.has_role('Developer')
#turn this into callable function \/
#async def getguild(ctx):
  #id = ctx.message.guild.id
  #print(id)
#async def getguild(ctx):
 # id = ctx.message.guild.id
 # print(id)

#web socket for Uptimerobot to ping, keeps bot online
keep_alive()
bot.run(os.environ['token'])