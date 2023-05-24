import discord
from discord import app_commands
from discord.ext import commands
import lists

class SlashCmds(commands.Cog,name="Slash Commands",description="SCMDS"):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot=bot
    
  @app_commands.command(name="command-1")
  async def my_command(self, inter: discord.Interaction) -> None:
    """ /command-1 """
    await inter.response.send_message("Hello from command 1!")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(SlashCmds(bot))
  #bot.tree.remove_command(SlashCmds.my_slash)
  #bot.tree.add_command(SlashCmds.my_slash,override=True)