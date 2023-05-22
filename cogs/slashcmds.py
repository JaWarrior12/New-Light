import discord
from discord import app_commands
from discord.ext import commands
import lists

class SlashCmds(commands.Cog,name="Slash Commands",description="Slash Commands, Nothing Here Right Now"):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot=bot

  async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.bot.tree.copy_global_to(guild=1031900634741473280)
        await self.bot.tree.sync(guild=1031900634741473280)
    
  @app_commands.command(name="slash")
  async def my_command(self,inter:discord.Interaction):
   # """ /command-1 """
    await inter.response.send_message("Hello from command 21!")

  @app_commands.command(name="testslash")
  @app_commands.choices(option=[app_commands.Choice(name="hi",value="gggg")])
  async def ts(self,inter:discord.Interaction,option:app_commands.Choice[str]):
    await inter.response.send_message(f'Name={option.name}; Value;{option.value}')

  @commands.command(name="ssc")
  async def ssc(self,ctx):
    tree=await self.bot.tree.sync()
    await ctx.send(f'Tree Synced! {len(tree)} commands synced!')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(SlashCmds(bot))