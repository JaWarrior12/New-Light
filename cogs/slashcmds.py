import discord
from discord import app_commands
from discord.ext import commands

class MyCog(commands.Cog,description="Slash Commands, Nothing Here Right Now"):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    
  @app_commands.command(name="slashb")
  async def my_command(self,ctx):
   # """ /command-1 """
    await ctx.send("Hello from command 1!")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))