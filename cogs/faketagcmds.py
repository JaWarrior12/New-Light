import os
import aiohttp
import discord 
import sys
from random import shuffle
import time
import ast
import pytz
import datetime
from datetime import time as tme
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
developers = lists.developers

submsMangrRleId=1245933318772490312 #Fake tag DB Submissions Manager Role ID

utc=datetime.timezone.utc
tmes=tme(hour=1,minute=0,tzinfo=utc)

class FakeTagCmds(commands.Cog, name="Fake Tag Database Commands",description="Access The Fake Tag Database, New Light's in-house fake tagged ship tracker."):
    def __init__(self, bot: commands.Bot):
        self.bot=bot
        if self.bot.user.id != 975858537223847936:
            self.fakeTagDBScanner.start()
            #pass
    def cog_unload(self):
        if self.bot.user.id != 975858537223847936:
            self.fakeTagDBScanner.cancel()
            #pass
        else:
            pass

    @commands.command(name="FakeTagDBStats",aliases=["ftdbstats"],brief="Stats On The Fake Tag Database")
    async def fakeTagDBStats(self,ctx):
        if str(ctx.message.author.id) not in banned:
            data=lists.readFile("faketagdb")["fakeTaggedShips"]
            e=discord.Embed(title="Fake Tag Database Stats")
            e.add_field(name="Number Of Ships Currently Tracked",value=len(data),inline=False)
            e.timestamp=datetime.datetime.now()
            await ctx.send(embed=e)
        else:
            await ctx.send("Your ID Is In The Banned List.")
  
    @commands.command(name="submitFakeTagger",aliases=["sft","addfaketag","submitft"],brief="Add A Fake Tagged Ship To The Database.")
    async def submitFakeTagger(self,ctx,hexcode,actualClansTag,*,shipName): #screenshot: discord.Attachment,
        if str(ctx.message.author.id) not in banned:
            data=lists.readFile("faketagdb")
            def find_route(data2, route_no):
                return list(filter(lambda y: y.get("hexcode") == str(route_no), data2))
            matchingHexs=find_route(data["fakeTaggedShips"],hexcode)
            if len(matchingHexs)>=1:
                submId=matchingHexs[0]["submissionId"]
                await ctx.send(f"The Hexcode {hexcode} has already been submitted in the submission with an ID of {submId}")
            else:
                try:
                    if len(ctx.message.attachments) >=1:
                        screenshoturl=ctx.message.attachments[0].url
                    else:
                        screenshoturl=None
                    id=data["currentId"]+1
                    data["currentId"]=id
                    existingTags=[]
                    for ship in data["fakeTaggedShips"]:
                        if ship["hexcode"] not in existingTags:
                            existingTags.append(ship["hexcode"])
                    if hexcode in existingTags:
                        await ctx.send(f"That Ship Is Already Registered")
                    else:
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
                        if len(ctx.message.attachments) >=1:
                            e.set_image(url=screenshoturl)
                        #tz = pytz.timezone('America/New_York')
                        e.timestamp=datetime.datetime.now()
                        await ctx.send(embed=e)
                        report={"submissionId":id,"hexcode":hexcode,"shipName":shipName,"screenshot":screenshoturl,"submitterName":ctx.message.author.name,"submitterId":ctx.message.author.id,"actualClansTag":actualClansTag,"submissionDate":date,"owner":None,"captains":[],"dateOfLastUpdate":date,"lastUpdatedBy":None,"formerShipNames":[]}
                        data["fakeTaggedShips"].append(report)
                        lists.setFile("faketagdb",data)
                except Exception as e:
                    await ctx.send(e)
        else:
            await ctx.send("Your ID Is In The Banned List.")

    @commands.command(name="scanFakeTagDB",aliases=["sftdb","searchft"],brief="!!CASE SENSITIVE!! Searches for the submission with the corresponding key:value pair.", help="Searches for the submission with the corresponding key:value pair. Valid Keys: submissionId, hexcode, shipName, actualClansTag, submissionDate & dateOfLastUpdate (EST, Format: MM-DD-YYYY; Day & Month can be single digits, year must be all four), submitterName (Name of user who submitted the ship), submitterId (ID of user who submitted the ship), screenshot (Value MUST Be A Discord Attachment URL)")
    async def scanFakeTagDB(self,ctx,key,value):
        if str(ctx.message.author.id) not in banned:
            validKeys=["submissionId","hexcode","shipName","actualClansTag","submissionDate","dateOfLastUpdate","submitterName","submitterId","screenshot","owner"]
            if key in validKeys:
                data=lists.readFile("faketagdb")["fakeTaggedShips"]
                def find_route(datab, route_no):
                    if key in ["submissionId","submitterId"]:
                        return list(filter(lambda y: y.get(key) == int(route_no), datab))
                    else:
                        return list(filter(lambda y: y.get(key) == route_no, datab))
                route = find_route(data,value)
                if len(route)==0:
                    await ctx.send(f"No Ships Found That Have A {key} of {value}.")
                else:
                    for x in route:
                        shipsFormerNames=""
                        for name in x["formerShipNames"]:
                            shipsFormerNames+="- "+name+"\n"
                        shipsCaptains=""
                        for captain in x["captains"]:
                            shipsCaptains+="- "+captain+"\n"
                        if len(shipsCaptains)==0:
                            shipsCaptains="None Submitted"
                        e = discord.Embed(title="Fake Tagged Ship Report")
                        e.add_field(name="Submission ID",value=x["submissionId"],inline=True)
                        e.add_field(name="Submission Date",value=x["submissionDate"],inline=True)
                        e.add_field(name="Date Of Last Update To Submission",value=x["dateOfLastUpdate"],inline=True)
                        e.add_field(name="Last Updated By",value=x["lastUpdatedBy"],inline=True)
                        e.add_field(name="Submitted By",value=x["submitterName"],inline=True)
                        e.add_field(name="@ Submitter",value=f"<@{x["submitterId"]}>",inline=True)
                        e.add_field(name="Ship Hexcode",value=x["hexcode"],inline=True)
                        e.add_field(name="Ship Name",value=x["shipName"],inline=True)
                        e.add_field(name="Tag Of The Clan That This Ship Actually Belongs To",value=x["actualClansTag"],inline=True)
                        e.add_field(name="Ship Owner",value=x["owner"],inline=True)
                        e.add_field(name="List Of Ship's Captains",value=shipsCaptains,inline=True)
                        e.add_field(name="List Of Ship's Former Names",value=shipsFormerNames,inline=True)
                        try:
                            e.set_image(url=x["screenshot"])
                        except:
                            pass
                        #tz = pytz.timezone('America/New_York')
                        e.timestamp=datetime.datetime.now()
                        await ctx.send(embed=e)
            else:
                await ctx.send(f"Sorry, But The Key Must Be One Of The Valid Keys. Valid Key List: {validKeys}")
        else:
            await ctx.send("Your ID Is In The Banned List.")
    
    @commands.command(name="updateFakeTagSubmission",aliases=["ufts"],brief="!!CASE SENSITIVE!! Updates the submission with the new corresponding key:value pair.", help="Searches for the submission with the corresponding key:value pair. Valid Keys: hexcode, shipName, actualClansTag, owner (Ship's Owner), captains (Captains on the ship)")
    async def scanFaketagDB(self,ctx,submissionId,key,*,value):
        if str(ctx.message.author.id) not in banned:
            validKeys=["shipName","actualClansTag","screenshot","owner","captains"]
            myguild = self.bot.get_guild(1031900634741473280)
            mychannel = myguild.get_channel(1245934187261722624)
            if key in validKeys:
                if key=="screenshot":
                    value=ctx.message.attachments[0].url
                data=lists.readFile("faketagdb")
                def find_route(data2, route_no):
                    return list(filter(lambda y: y.get("submissionId") == int(route_no), data2))
                route = find_route(data["fakeTaggedShips"], submissionId)
                if len(route)==0:
                    await ctx.send(f"No Ships Found That Have A submissionId of {submissionId}.")
                else:
                    for x in route:
                        submsnIndex=data["fakeTaggedShips"].index(x)
                        oldValue=x[key]
                        x[key]=value
                        shipsFormerNames=""
                        for name in x["formerShipNames"]:
                            shipsFormerNames+="- "+name+"\n"
                        data["fakeTaggedShips"][submsnIndex][key]=value
                        lastUpdater=x["lastUpdatedBy"]=f"{ctx.message.author.mention} ({ctx.message.author.name}/{ctx.message.author.id})"
                        data["fakeTaggedShips"][submsnIndex]["lastUpdatedBy"]=lastUpdater
                        if key=="shipName":
                            if value in data["fakeTaggedShips"][submsnIndex]["formerShipNames"] or value == data["fakeTaggedShips"][submsnIndex]["shipName"]:
                                await ctx.send(f"The Name {value} is already logged for the submission with an id of {submissionId}")
                                return
                            data["fakeTaggedShips"][submsnIndex]["formerShipNames"].append(oldValue)
                        if key=="captains":
                            print("captain update")
                            captainList=oldValue.copy()
                            print(f'Cap List: {captainList}')
                            if value not in captainList:
                                print("add cap")
                                captainList.append(value)
                            elif value in captainList:
                                print("remove cap")
                                captainList.remove(value)
                            else:
                                pass
                            x[key]=captainList
                            value=captainList
                            data["fakeTaggedShips"][submsnIndex]["captains"]=captainList
                            print(x[key])
                        shipsCaptains=""
                        for captain in x["captains"]:
                            shipsCaptains+="- "+captain+"\n"
                        if len(shipsCaptains)==0:
                            shipsCaptains="None Submitted"
                        tz = pytz.timezone('America/New_York')
                        date=f"{datetime.datetime.now(tz).month}-{datetime.datetime.now(tz).day}-{datetime.datetime.now(tz).year}"
                        data["fakeTaggedShips"][submsnIndex]["dateOfLastUpdate"]=date
                        e = discord.Embed(title="Fake Tagged Ship Report (Updated)")
                        e.add_field(name="Submission ID",value=x["submissionId"],inline=True)
                        e.add_field(name="Submission Date",value=x["submissionDate"],inline=True)
                        e.add_field(name="Date Of Last Update To Submission",value=date,inline=True)
                        e.add_field(name="Last Updated By",value=f"{ctx.message.author.mention} ({ctx.message.author.name}/{ctx.message.author.id})",inline=True)
                        e.add_field(name="Submitted By",value=x["submitterName"],inline=True)
                        e.add_field(name="@ Submitter",value=f"<@{x["submitterId"]}>",inline=True)
                        e.add_field(name="Ship Hexcode",value=x["hexcode"],inline=True)
                        e.add_field(name="Ship Name",value=x["shipName"],inline=True)
                        e.add_field(name="Tag Of The Clan That This Ship Actually Belongs To",value=x["actualClansTag"],inline=True)
                        e.add_field(name="Ship Owner",value=x["owner"],inline=True)
                        e.add_field(name="List Of Ship's Captains",value=shipsCaptains,inline=True)
                        e.add_field(name="List Of Ship's Former Names",value=shipsFormerNames,inline=True)
                        try:
                            e.set_image(url=x["screenshot"])
                        except:
                            pass
                        #tz = pytz.timezone('America/New_York')
                        e.timestamp=datetime.datetime.now()
                        await ctx.send(embed=e)
                        if key == "screenshot":
                            e.add_field(name=f"Screenshot Was Updated, Old Screenshot URL: {oldValue}",value=oldValue,inline=False)
                        elif key=="captains":
                            value=shipsCaptains
                            field_index = next(index for (index, f) in enumerate(e.fields) if f.value == value)
                            e.insert_field_at(field_index+1,name=f"Previous Value Of {key} (Item Directly Above)",value=oldValue,inline=False)
                        else:
                            field_index = next(index for (index, f) in enumerate(e.fields) if f.value == value)
                            e.insert_field_at(field_index+1,name=f"Previous Value Of {key} (Item Directly Above)",value=oldValue,inline=False)
                        await mychannel.send(embed=e)
                        lists.setFile("faketagdb",data)
            else:
                await ctx.send(f"Sorry, But The Key Must Be One Of The Valid Keys. Valid Key List: {validKeys}")
        else:
            await ctx.send("Your ID Is In The Banned List.")

    @commands.command(name="deleteFakeTagSubmission",aliases=["dfts"],brief="Deletes A Submission, Must Be The Orignial Submitter or a Fake Tag DB Submissions Manager to delete a submission.")
    async def deleteFakeTagSubmission(self,ctx,submissionId,*,reason):
        if str(ctx.message.author.id) not in banned:
            myguild = self.bot.get_guild(1031900634741473280)
            mychannel = myguild.get_channel(1245934187261722624)
            submsMngrRle=myguild.get_role(submsMangrRleId)
            data=lists.readFile("faketagdb")
            def find_route(data2, route_no):
                return list(filter(lambda y: y.get("submissionId") == int(route_no), data2))
            route = find_route(data["fakeTaggedShips"], submissionId)
            if len(route)==0:
                await ctx.send(f"No Ships Found That Have A submissionId of {submissionId}.")
            else:
                x=route[0]
                if (submsMngrRle in ctx.message.author.roles) or (ctx.message.author.id==x["submitterId"]) or (ctx.message.author.id in developers):
                    shipsFormerNames=""
                    for name in x["formerShipNames"]:
                        shipsFormerNames+="- "+name+"\n"
                    shipsCaptains=""
                    for captain in x["captains"]:
                        shipsCaptains+="- "+captain+"\n"
                    if len(shipsCaptains)==0:
                        shipsCaptains="None Submitted"
                    tz = pytz.timezone('America/New_York')
                    date=f"{datetime.datetime.now(tz).month}-{datetime.datetime.now(tz).day}-{datetime.datetime.now(tz).year}"
                    e = discord.Embed(title="Fake Tagged Ship Report (Deleted)")
                    e.add_field(name="Submission ID",value=x["submissionId"],inline=True)
                    e.add_field(name="Submission Date",value=x["submissionDate"],inline=True)
                    e.add_field(name="Date Of Last Update To Submission",value=x["dateOfLastUpdate"],inline=True)
                    e.add_field(name="Last Updated By",value=f"{ctx.message.author.mention} ({ctx.message.author.name}/{ctx.message.author.id})",inline=True)
                    e.add_field(name="Submitted By",value=x["submitterName"],inline=True)
                    e.add_field(name="@ Submitter",value=f"<@{x["submitterId"]}>",inline=True)
                    e.add_field(name="Ship Hexcode",value=x["hexcode"],inline=True)
                    e.add_field(name="Ship Name",value=x["shipName"],inline=True)
                    e.add_field(name="Tag Of The Clan That This Ship Actually Belongs To",value=x["actualClansTag"],inline=True)
                    e.add_field(name="Ship Owner",value=x["owner"],inline=True)
                    e.add_field(name="List Of Ship's Captains",value=shipsCaptains,inline=True)
                    e.add_field(name="List Of Ship's Former Names",value=shipsFormerNames,inline=True)
                    e.add_field(name="Submission Deletion Date",value=date,inline=False)
                    e.add_field(name="Submission Deleted By",value=f"{ctx.message.author.mention} ({ctx.message.author.name}/{ctx.message.author.id})",inline=False)
                    e.add_field(name="Reason For Submission Deletion",value=reason,inline=False)
                    try:
                        e.set_image(url=x["screenshot"])
                    except:
                        pass
                    #tz = pytz.timezone('America/New_York')
                    e.timestamp=datetime.datetime.now()
                    await ctx.send(f"The Submission With A submissionId Of {x["submissionId"]} has been DELETED")
                    await ctx.send(embed=e)
                    await mychannel.send(embed=e)
                    await mychannel.send("Restoration Dictonary (If Ever Needed)")
                    await mychannel.send(x)
                    data["fakeTaggedShips"].remove(x)
                    lists.setFile("faketagdb",data)
                else:
                    await ctx.send("Sorry, you need to be a Fake Tag DB Submissions Manager or the original submitter of the submission to be able to delete it.")
        else:
            await ctx.send("Your ID Is In The Banned List.")

    @commands.command(name="restoreFakeTagSubmission",aliases=["rfts"],brief="Restores A Fake Tag Submission By Use Of The Restoration Dictionary",disabled=True)
    async def restoreFakeTagSubmission(self,ctx,restorationDict):
        if str(ctx.message.author.id) not in banned:
            try:
                print(type(restorationDict))
                myguild = self.bot.get_guild(1031900634741473280)
                mychannel = myguild.get_channel(1245934187261722624)
                submsMngrRle=myguild.get_role(submsMangrRleId)
                data=lists.readFile("faketagdb")
                if (submsMngrRle in ctx.message.author.roles) or (ctx.message.author.id in developers):
                    restoreData=dict(restorationDict)
                    data["fakeTaggedShips"].append(restoreData)
                    index=data["fakeTaggedShips"].index(restoreData)
                    x=data["fakeTaggedShips"][index]
                    shipsFormerNames=""
                    for name in x["formerShipNames"]:
                        shipsFormerNames+="- "+name+"\n"
                    shipsCaptains=""
                    for captain in x["captains"]:
                        shipsCaptains+="- "+captain+"\n"
                    if len(shipsCaptains)==0:
                        shipsCaptains="None Submitted"
                    tz = pytz.timezone('America/New_York')
                    date=f"{datetime.datetime.now(tz).month}-{datetime.datetime.now(tz).day}-{datetime.datetime.now(tz).year}"
                    e = discord.Embed(title="Fake Tagged Ship Report (Deleted)")
                    e.add_field(name="Submission ID",value=x["submissionId"],inline=True)
                    e.add_field(name="Submission Date",value=x["submissionDate"],inline=True)
                    e.add_field(name="Date Of Last Update To Submission",value=x["dateOfLastUpdate"],inline=True)
                    e.add_field(name="Last Updated By",value=f"{ctx.message.author.mention} ({ctx.message.author.name}/{ctx.message.author.id})",inline=True)
                    e.add_field(name="Submitted By",value=x["submitterName"],inline=True)
                    e.add_field(name="@ Submitter",value=f"<@{x["submitterId"]}>",inline=True)
                    e.add_field(name="Ship Hexcode",value=x["hexcode"],inline=True)
                    e.add_field(name="Ship Name",value=x["shipName"],inline=True)
                    e.add_field(name="Tag Of The Clan That This Ship Actually Belongs To",value=x["actualClansTag"],inline=True)
                    e.add_field(name="Ship Owner",value=x["owner"],inline=True)
                    e.add_field(name="List Of Ship's Captains",value=shipsCaptains,inline=True)
                    e.add_field(name="List Of Ship's Former Names",value=shipsFormerNames,inline=True)
                    e.add_field(name="Submission Restoration Date",value=date,inline=False)
                    e.add_field(name="Submission Restored By",value=f"{ctx.message.author.mention} ({ctx.message.author.name}/{ctx.message.author.id})",inline=False)
                    lists.setFile("faketagdb",data)
                else:
                    await ctx.send("Sorry, you need to be a Fake Tag DB Submissions Manager or a Developer to be able to restore a submission.")
            except Exception as e:
                print(e)
                await ctx.send(e)
        else:
            await ctx.send("Your ID Is In The Banned List.")

    @commands.command(name="updateMajorClanList",aliases=["umcl"],brief="Updated List Of Current Major Clans When Scanning For Fake Tags",help="Updated List Of Current Major Clans When Scanning For Fake Tags. Viable Actions: add, remove, list")
    async def updateMajorClanList(self,ctx,action,tag=None,*,name=None):
        if ctx.message.author.id in developers:
            data=lists.readFile("faketagdb")
            def find_route(data2, route_no):
                return list(filter(lambda y: y.get("tag") == route_no, data2))
            route = find_route(data["currentMajorClans"], tag)
            if action=="list":
                for x in data["currentMajorClans"]:
                    await ctx.send(x)
            elif action=="add":
                data["currentMajorClans"].append({"name":name,"tag":tag})
                #await ctx.send(f"Added Clan `{name}` with Tag `{tag}`")
                lists.setFile("faketagdb",data)
            elif action=="remove":
                data["currentMajorClans"].remove(route[0])
                await ctx.send(f"Removed Clan `{route[0]["name"]}` with Tag `{route[0]["tag"]}`")
                lists.setFile("faketagdb",data)
            else:
                await ctx.send(f"Action of {action} is not valid. Valid Actions: list, add, remove.")
        else:
            await ctx.send(f'<@{ctx.message.author.id}> You Are NOT A Developer And CANNOT Use This Command')

    global tmes
    @tasks.loop(time=tmes)
    async def fakeTagDBScanner(self):
        if self.bot.application_id != 975858537223847936:
            try:
                print("Scanning For Fake Tags")
                def find_route(data2, route_no, key):
                    return list(filter(lambda y:route_no in y.get(key), data2))
                data=lists.readFile("faketagdb")
                def find_route2(data2, route_no, key):
                    return list(filter(lambda y: y.get(key) == route_no, data2))
                scanDates=data["datesToScan"]
                year=datetime.datetime.today().year
                month=datetime.datetime.today().month
                day=datetime.datetime.today().day
                namesUpdatedCount=0
                foundNames=[]
                async with aiohttp.ClientSession() as session:
                    jsondata = await lists.get_gzipped_json_aiohttp(session,f'https://pub.drednot.io/prod/econ/{year}_{month}_{day}/ships.json.gz')
                submittedHexs=[]
                for item in data["fakeTaggedShips"]:
                    submittedHexs.append(item["hexcode"])
                tags=[]
                shipdata=[]
                hexcodes=[]
                for x in data["currentMajorClans"]:
                    tags.append(x["tag"])
                for tag in tags:
                    ships = find_route(jsondata, tag, "name")
                    for ship in ships:
                        shipHex=str(ship["hex_code"].replace("{","").replace("}",""))
                        if shipHex not in hexcodes:
                            hexcodes.append(shipHex)
                            shipdata.append({"hexcode":shipHex,"names":[ship["name"]]})
                        else:
                            try:
                                target=shipdata.index(find_route2(shipdata, str(shipHex), "name")[0])
                                if ship["name"] not in shipdata[target]["names"]:
                                    shipdata[target]["names"].append(ship["name"])
                            except:
                                continue
                        if shipHex in submittedHexs:
                            targets=find_route2(shipdata, shipHex, "hexcode")
                            if len(targets)>=1:
                                targetb=targets[0]
                            else:
                                continue
                            target=shipdata.index(targetb)
                            subtar1=find_route2(data["fakeTaggedShips"], shipHex, "hexcode")[0]
                            subtar2={"hexcode":subtar1["hexcode"],"names":[subtar1["shipName"]]}
                            submittedtarget=data["fakeTaggedShips"].index(find_route2(data["fakeTaggedShips"], shipHex, "hexcode")[0])
                            shipsOldNames=[]
                            for name in shipdata[target]["names"]:
                                if name not in data["fakeTaggedShips"][submittedtarget]["formerShipNames"] and name != data["fakeTaggedShips"][submittedtarget]["shipName"]:
                                    data["fakeTaggedShips"][submittedtarget]["formerShipNames"].append(name)
                                    namesUpdatedCount+=1
                                    shipsOldNames.append(name)
                                    #print(name)
                            foundNames.append(f'Submission ID: {data["fakeTaggedShips"][submittedtarget]["submissionId"]}; List Of Alt Names Found: {shipsOldNames}')
                lists.setFile("faketagdb",data)
                print(f"Scan Complete, Total Number Of Names Found: {namesUpdatedCount}")
                for entry in foundNames:
                    pass
            except Exception as e:
                pass

    @fakeTagDBScanner.before_loop
    async def before_task_starts(self):
      await self.wait_until_ready()

async def setup(bot: commands.Bot):
  await bot.add_cog(FakeTagCmds(bot))
