import os, discord
from os import system
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

#Import Lists
import lists

lists.bannedlist()

intents = discord.Intents.default()
intents.members = True

client = discord.Client()

bot = commands.Bot(command_prefix='n!',intents=intents)

#SAVE THIS CODE \/!!!
#class MyHelp(commands.HelpCommand): 
    #async def send_bot_help(self, mapping):
      #channel = self.get_destination()
      #with open('Documentation.txt', 'rb') as fp:
         #await channel.send(file=discord.File(fp, 'New Light Documentation'))
        #f = open("Documentation.txt", "r")
        #if f.mode == 'r':
        #    contents = f.read()
        #    await channel.send("New Light Documentation")
        #    await channel.send(contents)

class MyHelp(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()

#bot.help_command = commands.DefaultHelpCommand() #MyHelp()

version = "3.2.0"

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    activity = discord.Game(name=f"JaWarrior.py & n!help. Version: {version}", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
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
  tz = pytz.timezone('America/New_York')
  ct = datetime.datetime.now(tz)
  print("Disconnected")
  #print(data)
  with open("Backups/disconnectlogs.txt", "a+") as o:
    o.write('\n')
    o.write(f'New Light disconnected from the DISCORD platform at {ct}.')
    o.write('\n')
  
#Load Cogs (My Way)
bot.load_extension("cogs.errorhand")
bot.load_extension("cogs.relcmds")
bot.load_extension("cogs.distcmds")
bot.load_extension("cogs.descmds")
bot.load_extension("cogs.qpcmds")
bot.load_extension("cogs.othercmds")
bot.load_extension("cogs.econcmds")
bot.load_extension("cogs.devcmds")

#Load Cogs Other Way
#extensions = ['DevCmds']

#if __name__ == '__main__':  # Ensures this is the file being ran
	#for extension in extensions:
		#bot.load_extension(extension)  # Loades every extension.

#web socket for Uptimerobot to ping, keeps bot online
keep_alive()
bot.run(os.environ['token'])