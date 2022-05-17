import os, discord
from keep_alive import keep_alive
from discord.ext import commands
from json import loads, dumps

authorized = [949451462151376948, 722703947638505556, 832250002562220062, 445763770799620097]
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
  
def readdata():
    return loads(open('distribution.json', 'r').read())


def setdata(data):
    with open("distribution.json", "w") as f:
        f.write(dumps(data))


def readdataB():
    return loads(open('relations.json', 'r').read())


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
      
def getships():
	return loads(open('designs.json','r').read())

@bot.command(name="logloot")
async def returnpaymentdata(ctx, *, msg):
    if ctx.message.author.id in authorized:
        msgparts, data = msg.split(" "), readdata()
        data[msgparts[0]][msgparts[1]] = int(msgparts[2])
        setdata(data)
        await ctx.send(f'now {msgparts[0]} has {msgparts[2]} {msgparts[1]}')
    else:
        await ctx.send('Unapproved Operator.')


@bot.command(name='reset')
async def resetalldata(ctx, *, msg):
    if ctx.message.author.id in authorized:
        data = readdata()
        for i in data[msg].keys():
            data[msg][i] = 0
        setdata(data)
        await ctx.send('User Data Reset')
    else:
        await ctx.send('Unapproved Operator.')


@bot.command(name='balance')
async def getuserloot(ctx, *, msg):
    await ctx.send(
        dumps(
            readdata()[msg]).replace(':','=').replace('{','').replace('}','').replace('"',''))


@bot.command(name='rel')
async def relations(ctx, *, msg):
    await ctx.send(
        dumps(readdataB()[msg]).replace(':', '=').replace('{', '').replace(
            '}', '').replace('"', ''))


@bot.command(name='qp')
@commands.has_role('QuickPing')
async def quickping(ctx, *, msg):
  await ctx.send(dumps(readdataC()[msg]).replace('{','').replace('}', '').replace('"', ''))


@quickping.error
async def quickping_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Error, Required Role: QuickPing, Not Found')

@bot.command(name='balall')
async def balanceall(ctx):
  if ctx.message.author.id in authorized:
    await ctx.send('Balances Of All Members')
    await ctx.send(dumps(readdata()).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"',''))
  else:
     await ctx.send('Unapproved Operator.')

@bot.command(name="changerel")
async def changerel(ctx, *, msg):
    if ctx.message.author.id in authorized:
        msgparts, data = msg.split(" "), readdataB()
        data[msgparts[0]] = str(msgparts[1])
        setdataB(data)
        await ctx.send(f'now {msgparts[0]} has a relation of {msgparts[1]}')
    else:
        await ctx.send('Unapproved Operator.')

@bot.command(name='calldes')
async def calldes(ctx,*,msg):
  msgparts, data = msg.split(" "), readdataD()
  data2 = msg.split(" ")
  a = "all"
  b = "category"
  if msg == a:
    await ctx.send(dumps(readdataD()).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n'))
  elif msgparts[0] == b:
    await ctx.send(dumps(readdataD()[msgparts[1]]).replace(': "',' = ').replace('{','').replace('}, ','\n').replace('}','').replace('"','').replace(',','\n'))
  else:
    await ctx.send('Your input does not match any command, for n!calldes please use n!calldes category "category" or n!calldes all to call specific design groups.')

@bot.command(name='addes')
@commands.has_role('OfficialMember')
async def savedesigns(ctx, *, msg):
  msgparts, data = msg.split(" "), readdataD()
  data[msgparts[0]][msgparts[1]] = str(msgparts[2])
  setdataD(data)
  await ctx.send(f'Added {msgparts[2]} to size {msgparts[1]} of type {msgparts[0]}')


    
#web socket for Uptimerobot to ping, keeps bot online
keep_alive()
bot.run(os.environ['token'])
