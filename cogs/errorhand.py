import os, discord
import time
import pytz
import datetime
import traceback
import sys
#from keep_alive import keep_alive
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup

import lists

class ErrorHandling(commands.Cog,description="New Light's Error Handler"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name="errorhandlist",hidden=True)
  async def ehl(self,ctx,msg=None):
    if ctx.message.author.id in lists.developers:
      if msg=="app":
        await ctx.send(self.has_app_command_error_handler)
      else:
        await ctx.send(self.has_error_handler)
    else:
      await ctx.send("Not A Dev")

  @commands.Cog.listener()
  async def on_command_completion(self,ctx):
    lists.logback(ctx,ctx.message.content)
    data=lists.readother()
    new=int(data["cmdcnt"])+1
    data["cmdcnt"]=int(new)
    lists.setother(data)

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
        #"""The event triggered when an error is raised while invoking a command.
        #Parameters
        #------------
        #ctx: commands.Context
            #The context used for command invocation.
        #error: commands.CommandError
            #The Exception raised.
        #"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} cannot be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error,commands.NoPrivateMessage):
          await ctx.send(f"{ctx.command} can only be used in a private message.")

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            #if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
            await ctx.send(f'Bad Argument: {error.param}')

        elif isinstance(error, commands.MissingRequiredArgument):
            #if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
              #pass
            await ctx.send(f'You are missing a required argument. Missing Argument: {error.param}')
              
        elif isinstance(error,commands.MissingRequiredAttachment):
          await ctx.send(f"A required attachment is missing. Missing Attachment: {error.param}")

        elif isinstance(error,commands.ExtensionAlreadyLoaded):
          await ctx.send(f"Extension {error.name} is already loaded.")

        elif isinstance(error,commands.ExtensionNotLoaded):
          await ctx.send(f"Extension {error.name} is not loaded.")

        elif isinstance(error,commands.ExtensionFailed):
          await ctx.send(f"Extension {error.name} failed. Original Exception: {error.original}")

        elif isinstance(error,commands.ExtensionNotFound):
          await ctx.send(f"Extension {error.name} was not found.")

        elif isinstance(error,commands.ExtensionError):
          await ctx.send("The requested Extension ran into an error.")

        elif isinstance(error,commands.ConversionError):
          await ctx.send(f"A Conversion has failed! COnverter:{error.converter}; Original:{error.original}")

        elif isinstance(error,commands.UserInputError):
          await ctx.send("The entered Key may not exist in that database. Please try another key.")
          
        elif isinstance(error,commands.MemberNotFound):
          await ctx.send(f'The requested Member could not be found. Missing Member: {error.argument}')

        elif isinstance(error,commands.UserNotFound):
          await ctx.send(f'The requested User could not be found. Missing User: {error.argument}')

        elif isinstance(error,commands.GuildNotFound):
          await ctx.send(f'The requested Guild could not be found. Missing Guild: {error.argument}')

        elif isinstance(error,commands.ChannelNotFound):
          await ctx.send(f'The requested Channel could not be found. Missing Channel: {error.argument}')
           
        elif isinstance(error,commands.MissingRole):
          await ctx.send(f'You do not have a role required to run this command. Missing Role: {error.missing_role}')

        elif isinstance(error,commands.BotMissingRole):
          await ctx.send(f'New Light does not have a role required to execute this command for you. Missing Role: {error.missing_role}')

        elif isinstance(error,commands.MissingPermissions):
          await ctx.send(f'You do not have the permissions required to run this command. Missing Role: {error.missing_permissions}')

        elif isinstance(error,commands.BotMissingPermissions):
          await ctx.send(f'New Light is missing permissions required to execute this command for you. Missing Role: {error.missing_permissions}')

        elif isinstance(error,commands.ChannelNotReadable):
          await ctx.send(f'The requested Channel could not be read because New Light is missing permissions to read messages in that channel. Channel Mentioned: {error.argument}')

        elif isinstance(error,commands.BadInviteArgument):
          await ctx.send(f'New Light Recived A Bad Invite, The Invite May Have Expired Or Was Just Bad.')

        elif isinstance(error,commands.TooManyArguments):
          await ctx.send(f'You have sent too many arguments for a command that does not take that many arguments. Please use n!help <command you just ran> for the help data for that command.')

        elif isinstance(error,commands.CommandOnCooldown):
          await ctx.send(f'The requested Command is on cooldown. Please Retry After {round(error.retry_after)} Seconds.')

        elif isinstance(error,commands.UnexpectedQuoteError):
          await ctx.send(f"A quote mark is missing! Quote: {error.quote}")

        elif isinstance(error,commands.InvalidEndOfQuoteStringError):
          await ctx.send(f"A quote has been closed incorrectly! Incorrect Character: {error.char}")

        elif isinstance(error,commands.ExpectedClosingQuoteError):
          await ctx.send(f"A quote mark is missing! Quote: {error.close_quote}")

        elif isinstance(error,commands.CheckFailure):
          await ctx.send(f'You have failed to pass the checks required to run {ctx.command}. This is the result of missing roles and/or permissions. Errors: {error.errors}; Failed Checks: {error.checks}')

        elif isinstance(error,app_commands.CommandSyncFailure):
          await ctx.send("App Command Error: Sync Failure")
          
        elif isinstance(error,app_commands.AppCommandError):
          await ctx.send("App Command Error: Sync Failure")
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

  @commands.Cog.listener()
  async def on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if hasattr(interaction.command, 'on_error'):
            return
          
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (app_commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error,app_commands.CommandSyncFailure):
          await interaction.response.send_message("App Command Error: Sync Failure")
          
        elif isinstance(error,app_commands.AppCommandError):
          await interaction.response.send_message("App Command Error: Sync Failure")
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(interaction.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

async def setup(bot: commands.Bot):
  await bot.add_cog(ErrorHandling(bot))