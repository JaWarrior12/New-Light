import os, discord
import time
import pytz
import datetime
import traceback
import sys
from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get
from discord import Member
from json import loads, dumps
from backup import backup
from startup import startup

class ErrorHandling(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

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

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')

        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send(f'You are missing a required argument. Missing Argument: {error.param}')

        elif isinstance(error,commands.ExtensionError):
          await ctx.send("The request Extension ran into an error.")

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

        elif isinstance(error,commands.CheckFailure):
          await ctx.send(f'You have failed to pass the checks required to run {ctx.command}. This is the result of missing roles and/or permissions. Errors: {error.errors}; Failed Checks: {error.checks}')
          
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot: commands.Bot):
  bot.add_cog(ErrorHandling(bot))