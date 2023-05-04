import os, discord
from os import system
import asyncio
import time
import pytz
import datetime 
from discord.ext import commands, tasks
from pretty_help import EmojiMenu, PrettyHelp
from discord.utils import get
from keep_alive import keep_alives
from discord import app_commands
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup
from dpyConsole import Console
import logging

#Import Lists
import lists

lists.bannedlist()

#handler=logging.basicConfig(filename='Backups/errorlog.log',format='%(asctime)s - %(levelname)s - %(message)s',filemode='a',level=logging.CRITICAL)
#logger = logging.getLogger()

intents = discord.Intents.all()
intents.members = True

#client = discord.Client()


bot = commands.Bot(command_prefix='n!',intents=intents)

value = bot

my_console = Console(bot)

nav = EmojiMenu("◀️", "▶️", "❌")
ending_note="New Light"
bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.green(),ending_note=ending_note)

class MyHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)
#bot.help_command = MyHelp()

version = "3.5.1"


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    activity = discord.Game(name=f"JaWarrior.py & n!help. Version: {version}", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await asyncio.sleep(5)
    #with open("images/bdaypic.png", "rb") as file:
      #image=file.read()
    #await bot.user.edit(avatar=image)
    await my_task.start()
    #lists.gidlist(bot)
    #channel = client.get_channel(974078794065403924)
    #await channel.send("I'm Logged In")

@bot.event
async def on_guild_join(guild):
  if int(guild.id) in lists.bannedGuild:
    await lists.checkguild(bot,guild)
  else:
    #guild=before
    tz = pytz.timezone('America/New_York')
    myguild = bot.get_guild(1031900634741473280)
    mychannel = myguild.get_channel(1037788623015268444)
    await mychannel.send(f'Joined Server: {guild.name}; ID: {guild.id}; Time:{datetime.dateime.now(tz)}')
    if guild.system_channel==None:
      invite="No System Channel Found, Unable To Create Invite"
    else:
      invite = await guild.system_channel.create_invite(reason="Inviting My Developer Incase You Need Support.")

    e = discord.Embed(title="I've joined a server.")
    e.add_field(name="Server Name", value=guild.name, inline=False)
    e.add_field(name="Invite Link", value=invite, inline=False)
    e.set_thumbnail(url=guild.icon)
    #tz = pytz.timezone('America/New_York')
    e.timestamp=datetime.datetime.now(tz)
    await mychannel.send(embed=e)
    await mychannel.send(f'Guild Name: {guild}')
    await mychannel.send(f'Guild Id: {guild.id}')

#@bot.event
#async def on_connect():
  #await bot.load_extension("cogs.errorhand")
  #await bot.load_extension("cogs.relcmds")
  #await bot.load_extension("cogs.distcmds")
  #await bot.load_extension("cogs.descmds")
  #await bot.load_extension("cogs.qpcmds")
  #await bot.load_extension("cogs.othercmds")
  #await bot.load_extension("cogs.econcmds")
  #await bot.load_extension("cogs.devcmds")
  #await bot.load_extension("cogs.adcmds")
  #await bot.load_extension("cogs.slashcmds")
  #await bot.load_extension("cogs.setupcmds")

@bot.event
async def on_disconnect():
  #if bot.is_closed() == True:
    tz = pytz.timezone('America/New_York')
    ct = datetime.datetime.now(tz)
    print("Disconnected")
    #print(data)
    with open("Backups/disconnectlogs.txt", "a+") as o:
      o.write(f'New Light disconnected from the DISCORD platform at {ct}.')
      o.write('\n\n')

@bot.event
async def on_guild_remove(guild):
  myguild = bot.get_guild(1031900634741473280)
  mychannel = myguild.get_channel(1037788623015268444)
  tz = pytz.timezone('America/New_York')
  await mychannel.send(f'Left Server: {guild.name}; ID: {guild.id}; Time:{datetime.dateime.now(tz)}')
  if guild.system_channel==None:
    invite="No System Channel Found, Unable To Create Invite"
  else:
    invite = await guild.system_channel.create_invite(reason="Notifying My Developer")
  lists.clearserver(str(guild.id))

  e = discord.Embed(title="I've Left A Server.")
  e.add_field(name="Server Name", value=guild.name, inline=True)
  e.add_field(name="Server ID",value=guild.id,inline=True)
  e.add_field(name="Invite Link", value=invite, inline=False)
  e.set_thumbnail(url=guild.icon)
  #tz = pytz.timezone('America/New_York')
  e.timestamp=datetime.datetime.now(tz)
  await mychannel.send(embed=e)
  await mychannel.send(f'Guild Name: {guild}')
  await mychannel.send(f'Guild Id: {guild.id}')
  lists.clrserver(guild.id)

@tasks.loop(seconds=30)
async def my_task():
  #print("loop")
  #print(my_task.next_iteration)
  data = lists.readother()
  chan=lists.readdataE()
  #myguild = bot.get_guild(1031900634741473280)
  #print(myguild)
  #channel = myguild.get_channel(1037788623015268444)
  #print(channel)
  #print(data)
  if len(data["pinglinks"]) == 0:
    pass
  else:
    #print(data["pinglinks"])
    for x in data["pinglinks"]:
      clan=x[0]
      link=x[1]
      pc=chan[str(clan)]["pingchan"]
      myguild = bot.get_guild(int(clan))
      print(int(clan))
      channel = myguild.get_channel(int(pc))
      print(channel)
      await channel.send(f'@here {link}')
      data["pinglinks"].remove(x)
      lists.setother(data)
    
#Load Cogs (My Way)
async def main():
  async with bot:
    await bot.load_extension("cogs.errorhand")
    await bot.load_extension("cogs.relcmds")
    await bot.load_extension("cogs.distcmds")
    await bot.load_extension("cogs.descmds")
    await bot.load_extension("cogs.qpcmds")
    await bot.load_extension("cogs.othercmds")
    await bot.load_extension("cogs.econcmds")
    await bot.load_extension("cogs.devcmds")
    await bot.load_extension("cogs.adcmds")
    await bot.load_extension("cogs.slashcmds")
    await bot.load_extension("cogs.setupcmds")
    #await tree.sync()
    my_console.start()
    await bot.start(os.environ['token'])
    #await my_task.start()


#Load Cogs Other Way
#extensions = ['DevCmds']

#if __name__ == '__main__':  # Ensures this is the file being ran
	#for extension in extensions:
		#bot.load_extension(extension)  # Loades every extension.

#web socket for Uptimerobot to ping, keeps bot online
#tree = app_commands.CommandTree(bot)
keep_alives()
#bot.run(os.environ['token'],log_handler=handler)
asyncio.run(main())
#@my_console.command()