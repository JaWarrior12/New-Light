import os, discord
import time
import pytz
import datetime
#from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from discord import Member
from discord import Permissions
from json import loads, dumps
from backup import backup
from startup import startup
import lists

banned= lists.banned

class FakeTagCmds(commands.Cog, name="Fake Tag Database Commands",description="Access The Fake Tag Database, New Light's in-house fake tagged ship tracker."):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_unload(self):
        pass
  
    @commands.command(name="submitFakeTagger",aliases=["sft","addfaketag"],brief="Add A Fake Tagged Ship To The Database.")
    async def submitFakeTagger(self,ctx,hexcode,actualClansTag,screenshot: discord.Attachment,*,shipName):
        if str(ctx.message.author.id) not in banned:
            try:
                #await ctx.send(screenshot.url)
                data=lists.readFakeTags()
                id=data["currentId"]+1
                tz = pytz.timezone('America/New_York')
                date=f"{datetime.datetime.now(tz).month}-{datetime.datetime.now(tz).day}-{datetime.datetime.now(tz).year}"
                e = discord.Embed(title="Fake Tagged Ship Report")
                hexcode=hexcode.replace("{","").replace("}","")
                e.add_field(name="Submission ID",value=id,inline=True)
                e.add_field(name="Submitted By",value=ctx.message.author.mention,inline=True)
                e.add_field(name="Ship Hexcode",value=hexcode,inline=True)
                e.add_field(name="Ship Name",value=shipName,inline=True)
                e.add_field(name="Tag Of The Clan That This Ship Actually Belongs To",value=actualClansTag,inline=True)
                e.add_field(name="Submission Date (EST)",value=date,inline=True)
                e.set_image(url=screenshot.url)
                #tz = pytz.timezone('America/New_York')
                e.timestamp=datetime.datetime.now()
                await ctx.send(embed=e)
                report={"submissionId":id,"hexcode":hexcode,"shipName":shipName,"screenshot":screenshot.url,"submitterName":ctx.message.author.name,"submitterId":ctx.message.author.id,"actualClansTag":actualClansTag,"date":date,"owner":None,"captains":[],"dateOfLastUpdate":date}
                data["fakeTaggedShips"].append(report)
                lists.setFakeTags(data)
            except Exception as e:
                await ctx.send(e)
        else:
            await ctx.send("Your ID Is In The Banned List.")

    @commands.command(name="scanFakeTaggedDB",aliases=["sftdb"],brief="!!CASE SENSITIVE!! Searches for the submission with the corresponding key:value pair.", help="Searches for the submission with the corresponding key:value pair. Valid Keys: submissionId, hexcode, shipName, actualClansTag, submissionDate & dateOfLastUpdate (EST, Format: MM-DD-YYYY; Day & Month can be single digits, year must be all four), submitterName (Name of user who submitted the ship), submitterId (ID of user who submitted the ship), screenshot (Value MUST Be A Discord Attachment URL)")
    async def scanFaketagDB(self,ctx,key,value):
        if str(ctx.message.author.id) not in banned:
            validKeys=["submissionId","hexcode","shipName","actualClansTag","submissionDate","dateOfLastUpdate","submitterName","submitterId","screenshot"]
            if key in validKeys:
                data=lists.readFakeTags()["fakeTaggedShips"]
                def find_route(data, route_no):
                    return list(filter(lambda x: x.get(key) == route_no, data))
                route = find_route(data,value)
                if len(route)==0:
                    await ctx.send(f"No Ships Found That Have A {key} of {value}.")
                else:
                    for x in route:
                        e = discord.Embed(title="Fake Tagged Ship Report")
                        e.add_field(name="Submission ID",value=x["submissionId"],inline=True)
                        e.add_field(name="Submission Date",value=x["submissionDate"],inline=True)
                        e.add_field(name="Date Of Last Update To Submission",value=x["dateOfLastUpdate"],inline=True)
                        e.add_field(name="Submitted By",value=x["submitterName"],inline=True)
                        e.add_field(name="@ Submitter",value=f"<@{x["submitterId"]}>",inline=True)
                        e.add_field(name="Ship Hexcode",value=x["hexcode"],inline=True)
                        e.add_field(name="Ship Name",value=x["shipName"],inline=True)
                        e.add_field(name="Tag Of The Clan That This Ship Actually Belongs To",value=x["actualClansTag"],inline=True)
                        e.add_field(name="Ship Owner",value=x["owner"],inline=True)
                        e.add_field(name="List Of Ship's Captains",value=x["captains"],inline=True)
                        e.set_image(url=x["screenshot"])
                        #tz = pytz.timezone('America/New_York')
                        e.timestamp=datetime.datetime.now()
                        await ctx.send(embed=e)
            else:
                await ctx.send(f"Sorry, But The Key Must Be One Of The Valid Keys. Valid Key List: {validKeys}")
        else:
            await ctx.send("Your ID Is In The Banned List.")
    
    @commands.command(name="updateFakeTagSubmission",aliases=["ufts"],brief="!!CASE SENSITIVE!! Updates the submission with the new corresponding key:value pair.", help="Searches for the submission with the corresponding key:value pair. Valid Keys: hexcode, shipName, actualClansTag, owner (Ship's Owner)")
    async def scanFaketagDB(self,ctx,submissionId,key,value):
        if str(ctx.message.author.id) not in banned:
            validKeys=["hexcode","shipName","actualClansTag","submissionDate","dateOfLastUpdate" ,"submitterName","submitterId","screenshot","owner"]
            if key in validKeys:
                data=lists.readFakeTags()["fakeTaggedShips"]
                def find_route(data, route_no):
                    return list(filter(lambda x: x.get("submissionId") == route_no, data))
                route = find_route(data, submissionId)
                if len(route)==0:
                    await ctx.send(f"No Ships Found That Have A submissionId of {submissionId}.")
                else:
                    for x in route:
                        e = discord.Embed(title="Fake Tagged Ship Report (Updated)")
                        e.add_field(name="Submission Id",value=x["submissionId"],inline=True)
                        e.add_field(name="Submitted By",value=x["submitterName"],inline=True)
                        e.add_field(name="@ Submitter",value=f"<@{x["submitterId"]}>",inline=True)
                        e.add_field(name="Ship Hexcode",value=x["hexcode"],inline=True)
                        e.add_field(name="Ship Name",value=x["shipName"],inline=True)
                        e.add_field(name="Tag Of The Clan That This Ship Actually Belongs To",value=x["actualClansTag"],inline=True)
                        e.add_field(name="Ship Owner",value=x["owner"],inline=True)
                        e.add_field(name="List Of Ship's Captains",value=x["captains"],inline=True)
                        e.set_image(url=x["screenshot"])
                        #tz = pytz.timezone('America/New_York')
                        e.timestamp=datetime.datetime.now()
                        await ctx.send(embed=e)
            else:
                await ctx.send(f"Sorry, But The Key Must Be One Of The Valid Keys. Valid Key List: {validKeys}")
        else:
            await ctx.send("Your ID Is In The Banned List.")

async def setup(bot: commands.Bot):
  await bot.add_cog(FakeTagCmds(bot))