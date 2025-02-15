import os, discord, sys
from tkinter import BooleanVar
from xmlrpc.client import boolean
from aiohttp import DataQueue
import time as timea
import traceback
import asyncio
import pytz
import datetime
from datetime import datetime, timedelta, timezone
from datetime import time as tme
#from apscheduler.schedulers.background import BackgroundScheduler
from threading import Timer
import urllib.request
import requests
import gzip
#from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.utils import get
from discord import Member
from json import loads, dumps
from startup import startup

# Translator Library
#from googletrans import Translator
from deep_translator import GoogleTranslator

#Lists
import lists
#Auth For Leadership Commands
#authorized = lists.authorized
banned = lists.banned
developers = lists.developers
DEV_SERVER_ID = lists.DEV_SERVER_ID 

#tz = pytz.timezone('America/New_York')
utc=timezone.utc
tmes=tme(hour=0,minute=10,tzinfo=utc)

class TranslationSystem(commands.Cog, name="Translation System Commands",description="Commands For The Translation System"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if self.bot.application_id == 974045822167679087:
            pass
    def cog_unload(self):
        if self.bot.application_id == 974045822167679087:
            pass
    
    @commands.command(name="translate", aliases=["tr"],help="Translates a piece of text. targetLang must be the 2 letter language code, OR the name of the language properly spelled.")
    async def translate(self, ctx, targetLang, text):
        translator = GoogleTranslator(source='auto', target=targetLang.lower())
        response=translator.translate(text=text)
        await ctx.send(response)

    @commands.command(name="configTranslate",aliases=["ct","configT"],help="Settings manager for all translation settings. `targetLang` MUST be the 2 letter language code!! When modifying a channel's settings, a value of `None`(Case Sensitive) will mark a setting that is not changed. Valid keys: list, add (Add channel), remove (Remove Channel), modify (Modify CHANNEL)")
    async def configTranslate(self,ctx,option,channel=None,targetLang=None,onBool=None):
        if str(ctx.message.author.id) not in banned:
            chk = lists.checkperms(ctx)
            if chk == True:
                data=lists.readFile("translationConfig")
                if option=="list":
                    e = discord.Embed(title="Translation Configuration Settings For "+ctx.message.guild.name)
                    e.add_field(name="Translation Active?",value=lists.readdataE()[str(ctx.message.guild.id)]["translationBool"],inline=False)
                    for item in data[str(ctx.message.guild.id)]["langChannels"]:
                        e.add_field(name="Channel Name",value=ctx.message.guild.get_channel(item[0]).name,inline=True)
                        e.add_field(name="Channel Mention",value=ctx.message.guild.get_channel(item[0]).mention,inline=True)
                        e.add_field(name="Channel ID",value=item[0],inline=True)
                        e.add_field(name="Target Language",value=item[1],inline=True)
                        e.add_field(name="Channel Actively Translated To?",value=item[3],inline=True)
                    await ctx.send(embed=e)
                elif option=="add":
                    chanID=None
                    chaneName=None
                    chanMen=None
                    if type(channel)==discord.TextChannel:
                        chanID=channel.id
                        chanName=channel.name
                        chanMen=channel.mention
                    elif type(channel)==str:
                        chanID=int(channel)
                        chanName=ctx.message.guild.get_channel(chanID).name
                        chanMen=ctx.message.guild.get_channel(chanID).mention
                    else:
                        return await ctx.send(f"Sorry, {channel} is not a valid input. Please mention your target channel or use the channel's ID.")
                    if len(targetLang)==2:
                        pass
                    else:
                        return await ctx.send(f"Sorry, {targetLang} is not a valid input. Please provide the 2 letter language code for your target language.")
                    data[str(ctx.message.guild.id)]["langChannels"].append([int(chanID),targetLang,True])
                    data[str(ctx.message.guild.id)]["langChanIDs"].append(int(chanID))
                    lists.setFile("translationConfig",data)
                    await ctx.send(f"{chanMen} has been added to Auto-Translate for the target language {targetLang}")
                elif option=="remove":
                    chanID=None
                    chaneName=None
                    chanMen=None
                    if type(channel)==discord.TextChannel:
                        chanID=channel.id
                        chanName=channel.name
                        chanMen=channel.mention
                    elif type(channel)==int:
                        chanID=channel
                        chanName=ctx.message.guild.get_channel(chanID).name
                        chanMen=ctx.message.guild.get_channel(chanID).mention
                    else:
                        return await ctx.send(f"Sorry, {channel} is not a valid input. Please mention your target channel or use the channel's ID.")
                    indexToRemove=None
                    for chan in data[str(ctx.message.guild.id)]["langChannels"]:
                        if chan[0]==int(chanID):
                            indexToRemove = data[str(ctx.message.guild.id)]["langChannels"].index(chan)
                    data[str(ctx.message.guild.id)]["langChannels"].pop(indexToRemove)
                    lists.setFile("translationConfig",data)
                elif option=="modify":
                    chanID=None
                    chaneName=None
                    chanMen=None
                    if type(channel)==discord.TextChannel:
                        chanID=channel.id
                        chanName=channel.name
                        chanMen=channel.mention
                    elif type(channel)==str:
                        chanID=channel
                        chanName=ctx.message.guild.get_channel(int(chanID)).name
                        chanMen=ctx.message.guild.get_channel(int(chanID)).mention
                    index=None
                    for chan in data[str(ctx.message.guild.id)]["langChanIDs"]:
                        if chan==int(chanID):
                            index = data[str(ctx.message.guild.id)]["langChanIDs"].index(chan)
                    if targetLang.lower()!="none" and len(targetLang)==2:
                        data[str(ctx.message.guild.id)]["langChannels"][index][1]=targetLang
                    if onBool!="none":
                        boolVal=False
                        if onBool.lower() in ["true","yes","on","1","True"]:
                            boolVal=True
                        elif onBool.lower() in ["false","no","off","0","False"]:
                            boolVal=False
                        else:
                            return await ctx.send(f"Sorry, {onBool} is not a valid input. Please use `True` or `False`.")
                        data[str(ctx.message.guild.id)]["langChannels"][index][2]=boolVal
                    lists.setFile("translationConfig",data)
                    await ctx.send(f"Settings for {chanMen} have been modified.")
                else:
                    await ctx.send(f"Sorry, `{option}` is not a Valid Option. Valid Options: `add`, `remove`, `list`, `modify`.")
            else:
                await ctx.send("Sorry, only authorized leaders can use this command.")
        else:
            await ctx.send("Sorry, You are banned from using New Light. Contact JaWarrior if you believe this to be a mistake.")

    @commands.Cog.listener()
    async def on_message(self,message):
        #print("Message Received, Translating...")
        server=message.guild
        data=lists.readFile("translationConfig")
        #print(message.author.bot)
        #print(message)
        #print(message.attachments)
        #print(message.webhook_id)
        #print(bool(int(message.webhook_id)>0))
        if message.author.bot or bool(int(message.webhook_id)>0):
            return
        if message.guild!=None and lists.readdataE()[str(server.id)]["translationBool"]:
            if int(message.channel.id) in data[str(server.id)]["langChanIDs"]:
                translator = GoogleTranslator(source='auto', target='russian')
                langChannels=data[str(server.id)]["langChannels"]
                try:
                    for channel in langChannels:
                        attachments=None
                        fileNames=None
                        if message.attachments!=None:
                            attachments=[]
                            fileNames=[]
                            for attachment in message.attachments:
                                saved=await attachment.to_file()
                                fileNames.append(saved.filename)
                                attachments.append(saved)
                        chanID=channel[0]
                        targetLang=channel[1]
                        targetChanBool=channel[2]
                        if targetChanBool and (message.channel.id!=chanID):
                            targetChan=server.get_channel(chanID)
                            translator.target=str(targetLang)
                            #response=translator.translate(text=message.content)
                            if message.reference is not None:
                                fullText=f"From {message.author.mention}: \nReplying to {message.reference.resolved.author.mention}: {message.content}" 
                                response=translator.translate(text=fullText)
                                sentMsg=await targetChan.send("Translating Reply...",embeds=message.embeds,files=attachments,silent=True,stickers=message.stickers)
                                await sentMsg.edit(content=response)
                            else:
                                fullText=f"From {message.author.mention}: {message.content}"
                                response=translator.translate(text=fullText)
                                sentMsg=await targetChan.send("Translating Reply...",embeds=message.embeds,files=attachments,silent=True,stickers=message.stickers)
                                await sentMsg.edit(content=response)
                        else:
                            pass
                except Exception as e:
                    print(e)
                    e_type, e_object, e_traceback = sys.exc_info()

                    e_filename = os.path.split(
                        e_traceback.tb_frame.f_code.co_filename
                    )[1]

                    e_message = str(e)

                    e_line_number = e_traceback.tb_lineno

                    print(f'exception type: {e_type}')

                    print(f'exception filename: {e_filename}')

                    print(f'exception line number: {e_line_number}')

                    print(f'exception message: {e_message}')
    

async def setup(bot: commands.Bot):
    await bot.add_cog(TranslationSystem(bot))