import os, discord
from os import system
import asyncio
import time
import pytz
import datetime 
from discord.ext import commands, tasks
from discord.utils import get
from keep_alive import keep_alives
from discord import app_commands
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup
from dpyConsole import Console

#Import Lists
import lists

lists.bannedlist()

intents = discord.Intents.all()
intents.members = True

#client = discord.Client()



bot = commands.Bot(command_prefix='n!',intents=intents)

value = bot

my_console = Console(bot)

class MyHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)


#class MyHelp(commands.MinimalHelpCommand):
    #async def send_bot_help(self, mapping):
        #embed = discord.Embed(title="Help")
        #for cog, commands in mapping.items():
           #filtered = await self.filter_commands(commands, sort=True)
           #command_signatures = [self.get_command_signature(c) for c in filtered]
           #if command_signatures:
                #cog_name = getattr(cog, "qualified_name", "No Category")
                #embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        #channel = self.get_destination()
        #await channel.send(embed=embed)

bot.help_command = MyHelp()

#bot.help_command = commands.DefaultHelpCommand() #MyHelp()

#bot.remove_command('help')

version = "3.4.0"


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    activity = discord.Game(name=f"JaWarrior.py & n!help. Version: {version}", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await asyncio.sleep(5)
    await my_task.start()
    #channel = client.get_channel(974078794065403924)
    #await channel.send("I'm Logged In")

@bot.event
async def on_guild_join(guild):
    #guild=before
    myguild = bot.get_guild(1031900634741473280)
    channel = myguild.get_channel(1037788623015268444)
    invite = await guild.system_channel.create_invite(reason="Inviting My Developer To Your Amazing Server!")

    e = discord.Embed(title="I've joined a server.")
    e.add_field(name="Server Name", value=guild.name, inline=False)
    e.add_field(name="Invite Link", value=invite, inline=False)
    e.set_thumbnail(url=guild.icon_url)
    await channel.send(embed=e)
    await channel.send(f'Guild Name: {guild}')
    await channel.send(f'Guild Id: {guild.id}')

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

@tasks.loop(seconds=30)
async def my_task():
  #print(my_task.next_iteration)
  data = lists.readother()
  chan=lists.readdataE()
  #myguild = bot.get_guild(1031900634741473280)
  #print(myguild)
  #channel = myguild.get_channel(1037788623015268444)
  #print(channel)
  #print(data)
  if len(data["pinglinks"]) == 0:
    return False
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
asyncio.run(main())

#@my_console.command()