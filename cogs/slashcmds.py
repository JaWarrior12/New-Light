import discord
from discord import app_commands
from discord.ext import commands

class SlashCmds(commands.Cog,name="Slash Commands",description="Slash Commands, Nothing Here Right Now"):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot=bot
    
  @app_commands.command(name="slash")
  async def my_command(self,inter:discord.Interaction):
   # """ /command-1 """
    await inter.response.send_message("Hello from command 1!")

  @commands.command(name="ssc")
  async def ssc(self,ctx):
    await self.bot.tree.sync()
    print(1)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(SlashCmds(bot))