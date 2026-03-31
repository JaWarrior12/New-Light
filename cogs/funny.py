import os
import discord
import time
import asyncio
from flask import ctx
import pytz
import re
import random
import datetime
from datetime import time as timed
from datetime import timezone
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from discord import Member
from discord import Permissions
from json import loads, dumps
from backup import backup
from startup import startup

#Lists
import lists
#import main
#Auth For Leadership Commands
#authorized = lists.authorized
banned = lists.banned
developers = lists.developers

utc=timezone.utc
times=timed(hour=0,minute=20,tzinfo=utc)

# Pinkemic Role System (Color Role Fun)
PinkemicEnabled = False
PinkRoleId=1384384321074233434
INFECTION_CHANCE = 0.05  # 5%
KEYWORDS = ["pink","purple","brute","alt","job","work","yellow","https"]  # Infection keywords
STOPWORDS = {
    "the", "and", "you", "that", "this", "with", "have", "for",
    "not", "are", "but", "was", "from", "they", "your"
}
WORD_REGEX = r"\b[a-zA-Z]{4,}\b"
BLACKLISTED_WORDS = ["cureme"]

# Rainbow Role System
RainbowEnabled = True
RainbowColors = [
    0xFF0000,  # red
    0xFF7F00,  # orange
    0xFFFF00,  # yellow
    0x00FF00,  # green
    0x0000FF,  # blue
    0x4B0082,  # indigo
    0x8B00FF   # violet
]
allowed_role_id = 1376827779093495838
RainbowRoleId=1487128561214296267

class FunnyStuff(commands.Cog, name="Funnys",description="Hehe funny"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.file_lock = asyncio.Lock() # Pinkedemic
        self.running = {} # Rainbow Role
        global PinkemicEnabled
        PinkemicEnabled = loads(open(f'funny.json', 'r').read())["infectionEnabled"]
    def cog_unload(self):
        pass
    
#------------ Pinkedemic Role -----------#
    @commands.Cog.listener()
    async def on_messageq(self, msg):
        if PinkemicEnabled == True:
            try:
                if msg.author.bot or not msg.guild:
                    return

                if msg.guild.id != 1070759679543750697:
                    return

                data = loads(open(f'funny.json', 'r').read())

                if "pinked" not in data:
                    data["pinked"] = []
                
                if "pink_spread_stats" not in data:
                    data["pink_spread_stats"] = {
                        "total_infections": 0,
                        "current_pinked": 0,
                        "reply_infections": 0,
                        "random_infections": 0,
                        "keyword_infections": 0
                    }

                stats = data["pink_spread_stats"]
                vectors = data.get("infection_vectors", {})

                pinked_ids = [
                    user["id"] if isinstance(user, dict) else user
                    for user in data["pinked"]
                ]

                # 🔥 Roll infection chance
                chance = data.get("infection_chance", 0.15)
                if random.random() < chance and vectors.get("random", True):
                    role = msg.guild.get_role(1384384321074233434)

                    #if role and role not in msg.author.roles:
                    #    await msg.author.add_roles(role, reason="Pinkedemic")

                    # Add to list if not already there
                    user_entry = next(
                        (u for u in data["pinked"] if u["id"] == msg.author.id),
                        None
                    )
                    if user_entry and not user_entry.get("immunity", False):
                        if not any(u["id"] == msg.author.id for u in data["pinked"]):
                            stats["random_infections"] += 1
                            stats["total_infections"] += 1
                            await add_to_pinklist(self, msg.author, data, "random chance") 
                            #await send_infection_log(self, msg.author, "random chance")

                # 🔍 Check if message is a reply
                if msg.reference and vectors.get("reply", True):
                    replied_message = msg.reference.resolved
                    if replied_message is None:
                        replied_message = await msg.channel.fetch_message(msg.reference.message_id)

                    replied_user = replied_message.author
                    
                    user_entry = next(
                        (u for u in data["pinked"] if u["id"] == replied_user.id),
                        None
                    )
                    if user_entry and not user_entry.get("immunity", False):
                        if replied_user.id in pinked_ids and random.random() < data.get("reply_chance", 0.75):
                            #print("Spreading infection!")

                            # Infect the author
                            if msg.author.id not in pinked_ids:
                                stats["reply_infections"] += 1
                                stats["total_infections"] += 1
                                #with open(f'funny.json', "w") as f:
                                #    f.write(dumps(data))
                                await add_to_pinklist(self, msg.author, data, "reply infection")

                            role = msg.guild.get_role(1384384321074233434)

                            #if role and role not in msg.author.roles:
                            #    await msg.author.add_roles(role, reason="Pinkedemic")
                                #await send_infection_log(self, msg.author, "reply infection")
                            
                # 🔔 Infection via Mention
                if vectors.get("mention", True) and msg.mentions:
                    role = msg.guild.get_role(1384384321074233434)
                    # Get infected user IDs
                    infected_ids = [
                        u["id"] if isinstance(u, dict) else u
                        for u in data.get("pinked", [])
                    ]
                    # Loop through mentions
                    for mentioned_user in msg.mentions:
                        # Skip bots
                        if mentioned_user.bot:
                            continue
                        # Check if the mentioned user is infected
                        user_entry = next(
                            (u for u in data["pinked"] if u["id"] == mentioned_user.id),
                        None
                        )
                        if user_entry and not user_entry.get("immunity", False):
                            if mentioned_user.id in infected_ids:
                                #print("Mention infection triggered!")
                                # 🎲 Infection chance (configurable)
                                if random.random() < data.get("mention_chance", 0.75):
                                    #if role and role not in msg.author.roles:
                                    #    await msg.author.add_roles(role, reason="Pinkedemic (ping infected user)")
                                    # Add to infected list if not already there
                                    if not any((u["id"] if isinstance(u, dict) else u) == msg.author.id
                                            for u in data["pinked"]
                                        ):
                                        stats["mention_infections"] = stats.get("mention_infections", 0) + 1
                                        stats["total_infections"] += 1
                                        await add_to_pinklist(self, msg.author, data, "mention infection")
                                    # 📊 Stats tracking (scalable)
                                    break  # prevent multiple infections from one message
                           
                if vectors.get("keyword", True): 
                    #print("Checking for keyword infection...")
                    message = msg.content.lower()
                    # Normalize infected IDs safely
                    infected_ids = [
                        (u["id"] if isinstance(u, dict) else u)
                        for u in data.get("pinked", [])
                    ]

                    already_infected = msg.author.id in infected_ids
                    
                    user_entry = next(
                        (u for u in data["pinked"] if u["id"] == msg.author.id),
                        None
                    )
                    if user_entry and not user_entry.get("immunity", False):
                        # ----------------------------
                        # 🔒 HARDCODED KEYWORDS (ALWAYS TRIGGER)
                        # ----------------------------

                        try:
                            for keyword in KEYWORDS:
                                if keyword in message and not already_infected:
                                    #print("Keyword infection triggered!")
                                    if not any(u["id"] == msg.author.id for u in data["pinked"]):
                                        stats["keyword_infections"] = stats.get("keyword_infections", 0) + 1
                                        stats["total_infections"] += 1
                                        await add_to_pinklist(self, msg.author, data, f"hardcoded: {keyword}")
                                        break  # prevent multiple keyword infections from one message

                            # ----------------------------
                            # 🧬 DYNAMIC KEYWORDS
                            # ----------------------------
                            if vectors.get("dynamic_keywords", True):
                                active_keywords = data.get("infection_keywords", {}).get("active", [])

                                for keyword in active_keywords:
                                    if keyword in message and not already_infected and keyword not in BLACKLISTED_WORDS:
                                        if not any(u["id"] == msg.author.id for u in data["pinked"]):
                                            stats["keyword_infections"] = stats.get("keyword_infections", 0) + 1
                                            stats["total_infections"] += 1
                                        await add_to_pinklist(self, msg.author, data, f"keyword: {keyword}")
                                        break  # prevent multiple infections from one message
                        except Exception as e:
                            print(f"Error checking keywords: {e}")
                            import traceback
                            traceback.print_exc()

                # Ensure structures exist
                data.setdefault("word_scores", {})
                data.setdefault("infection_keywords", {
                    "active": ["pink"],
                    "history": [],
                    "threshold": 10,
                    "max_active": 5
                })

                # 🔍 Get user entry
                user_entry = next(
                    (u for u in data.get("pinked", [])
                        if isinstance(u, dict) and u.get("id") == msg.author.id),
                    None
                )

                # ----------------------------
                # 🧬 UPDATE WORD SCORES
                # ----------------------------
                if user_entry:
                    words = self.extract_words(msg.content)
                    self.update_word_scores(data, words, user_entry)

                # ----------------------------
                # 📉 DECAY
                # ----------------------------
                self.decay_word_scores(data)

                # ----------------------------
                # 🔁 PROMOTE
                # ----------------------------
                self.promote_keywords(data)

                # ----------------------------
                # ☣️ CHECK INFECTION
                # ----------------------------
                await self.check_keyword_infection(msg, data)

                # ----------------------------
                # 💾 SAVE
                # ----------------------------
                #with open('funny.json', 'w') as f:
                #    f.write(dumps(data, indent=4))

            except Exception:
                import traceback
                traceback.print_exc()
                
    @commands.Cog.listener()
    async def on_reaction_addq(self, reaction, user):
        if PinkemicEnabled == True:
            try:
                if user.bot:
                    return

                data = loads(open(f'funny.json', 'r').read())

                guild = reaction.message.guild
                if not guild or guild.id != 1070759679543750697:
                    return

                vectors = data.get("infection_vectors", {})
                stats = data.get("pink_spread_stats", {})

                if not vectors.get("reaction", True):
                    return

                role = guild.get_role(1384384321074233434)
                if not role:
                    return

                # 🔍 Check if message author is infected
                infected_ids = [u["id"] if isinstance(u, dict) else u for u in data.get("pinked", [])]

                user_entry = next(
                        (u for u in data["pinked"] if u["id"] == reaction.message.author.id),
                        None
                    )
                if user_entry and not user_entry.get("immunity", False):
                    if reaction.message.author.id in infected_ids:
                        # 🎲 Infection chance
                        if random.random() < data.get("reaction_chance", 0.2):

                            #if role not in user.roles:
                            #    await user.add_roles(role, reason="Pinkedemic")

                            if user.id not in infected_ids:
                                stats["reaction_infections"] = stats.get("reaction_infections", 0) + 1
                                stats["total_infections"] += 1
                                await add_to_pinklist(self, user, data, "reaction infection")
                                #send_infection_log(self, user, "reaction infection")

            except Exception as e:
                print(e)
                
    @commands.Cog.listener()
    async def on_member_joinq(self, member):
        try:
            if member.guild.id != 1070759679543750697:
                return

            data = loads(open(f'funny.json', 'r').read())

            if "pinked" not in data:
                return

            # Get stored infected IDs
            infected_ids = [
                user["id"] if isinstance(user, dict) else user
                for user in data["pinked"]
            ]
            
                # 🔍 Find user entry safely (handles dicts + old ints)
            user_entry = next(
                (
                    u if isinstance(u, dict) else {"id": u, "hidden_carrier": False}
                    for u in data["pinked"]
                    if (u["id"] if isinstance(u, dict) else u) == member.id
                ),
                None
            )

            if not user_entry:
                return

            # 🚫 Skip hidden carriers
            if user_entry.get("hidden_carrier", False):
                return

            if member.id in infected_ids:
                role = member.guild.get_role(1384384321074233434)

                if role and not user_entry.get("immunity", False):
                    await member.add_roles(role, reason="Pinkedemic rejoin restore")

        except Exception as e:
            print(e)
                    
    @commands.Cog.listener()
    async def on_member_updateq(self, before, after):
        if PinkemicEnabled == True:
            if not after.guild or after.guild.id != 1070759679543750697:
                return
            try:
                data = loads(open(f'funny.json', 'r').read())
                #print(data)
                if any(user["id"] == after.id for user in data["pinked"]):

                    user_entry = next(
                        (
                            u if isinstance(u, dict) else {"id": u, "hidden_carrier": False}
                            for u in data["pinked"]
                            if (u["id"] if isinstance(u, dict) else u) == after.id
                        ),
                        None
                    )
                    
                    role = after.guild.get_role(PinkRoleId)
                    if not role:
                        return

                    # 🔑 Only trigger if the role was REMOVED
                    # 🚫 Skip hidden carriers
                    if user_entry.get("hidden_carrier", False):
                        return

                    if role in before.roles and role not in after.roles and not user_entry.get("immunity", False):
                        await after.add_roles(role, reason="Pinkedemic")
            except Exception as e:
                print(e)
            
    @commands.command(name="cureAllq")
    async def clearpinked(self, ctx):
        # 🔒 Permission check
        if ctx.message.author.id not in developers:
            await ctx.send("You can't use this command.")
            return
        #if not any(r.id == allowed_role_id for r in ctx.author.roles):
        #    await ctx.send("You don't have permission.")
        #    return
        global PinkemicEnabled
        PinkemicEnabled = False # Temporarily
        
        data = loads(open(f'funny.json', 'r').read())
        data["infectionEnabled"] = False

        if "pinked" not in data or not data["pinked"]:
            await ctx.send("Pinked list is already empty.")
            return

        role = ctx.guild.get_role(PinkRoleId)
        if not role:
            await ctx.send("Role not found.")
            return

        removed_count = 0

        for user in data["pinked"]:
            user_id = user["id"]  # ✅ extract the actual ID
            try:
                member = await ctx.guild.fetch_member(user_id)
                if not member:
                    continue

                if role in member.roles:
                    await member.remove_roles(role, reason="Pinkedemic cleared")
                    removed_count += 1

            except Exception as e:
                print(e)

        # 🧹 Clear the list
        data["pinked"] = []
        
        # 📊 Reset stats dynamically (no hardcoding)
        stats = data.get("pink_spread_stats", {})

        for key in stats.keys():
            stats[key] = 0
        
        with open(f'funny.json', "w") as f:
            f.write(dumps(data))

        await ctx.send(f"🌸 Pinkedemic cleared! Removed role from {removed_count} users.")
        
    @commands.command()
    async def infectq(self, ctx):
        # 🔒 permission check
        if ctx.message.author.id not in developers:
            await ctx.send("You can't use this command.")
            return
        #if not any(r.id == allowed_role_id for r in ctx.author.roles):
        #    await ctx.send("You don't have permission.")
        #    return

        role = ctx.guild.get_role(PinkRoleId)
        if not role:
            await ctx.send("Pink role not found.")
            return

        # 🎯 Get online members (exclude bots + self)
        members = [
            m for m in ctx.guild.members
            if not m.bot
            and m.status != discord.Status.offline
            and role not in m.roles
        ]

        if not members:
            await ctx.send("No valid targets found.")
            return

        target = random.choice(members)

        global PinkemicEnabled
        PinkemicEnabled = True # Ensure it's enabled when infecting
        
        try:
            await target.add_roles(role, reason="Pinkedemic infection")
            await ctx.send(f"🦠 {target.mention} has been infected!")

            # 🧠 Add to your pinked list
            data = loads(open(f'funny.json', 'r').read())
            data["infectionEnabled"] = True

            if "pinked" not in data:
                data["pinked"] = []

            if not any(u["id"] == target.id if isinstance(u, dict) else u == target.id for u in data["pinked"]):
                await add_to_pinklist(self, target, data, "Pinkedemic")

        except Exception as e:
            print(e)
            await ctx.send("Failed to infect target.")
            
    @commands.command(name="enablePinkedemicq")
    async def enable_pinkedemicq(self, ctx):
        if ctx.message.author.id not in developers:
            await ctx.send("You can't use this command.")
            return
        # 🔒 Permission check
        #if not any(r.id == allowed_role_id for r in ctx.author.roles):
        #    await ctx.send("You don't have permission.")
        #    return
        global PinkemicEnabled
        PinkemicEnabled = True
        await ctx.send("Pinkedemic enabled! Spread the pink!")
        
    @commands.command()
    async def pinkstatsq(self, ctx):
        if ctx.message.author.id not in developers:
            await ctx.send("You can't use this command.")
            return
        try:
            data = loads(open(f'funny.json', 'r').read())
            stats = data.get("pink_spread_stats", {})

            # Build message dynamically
            lines = ["🦠 **Pinkedemic Stats** 🦠\n"]

            # Always show these first if they exist
            important_keys = ["total_infections", "current_pinked"]

            for key in important_keys:
                if key in stats:
                    formatted = key.replace("_", " ").title()
                    lines.append(f"📊 {formatted}: {stats[key]}")

            lines.append("\n📈 **Infection Vectors:**")

            # Show everything else dynamically
            for key, value in stats.items():
                if key in important_keys:
                    continue

                formatted = key.replace("_", " ").title()
                lines.append(f"• {formatted}: {value}")

            message = "\n".join(lines)

            try:
                await ctx.author.send(message)
                await ctx.reply("📬 I’ve sent your stats in DMs!", delete_after=5)
            except Exception:
                await ctx.reply("❌ I couldn't DM you.")

        except Exception as e:
            print(e)
            
    @commands.command(name="cureMeq", hidden=True,disabled=True)
    async def cure_meq(self, ctx):
        data = loads(open(f'funny.json', 'r').read())
        if not data["global_cure"].get("cure_enabled", False):
            await ctx.send("Curing is not currently enabled.")
            return
        else:
            if ctx.guild.id != 1070759679543750697:
                return
            await ctx.send("Attempting to cure you...")
            await cure_user(self, ctx, ctx.author)
    
#----------------Rainbow Role----------------#
    @commands.command()
    async def rainbow(self, ctx, member: commands.MemberConverter):
        global RainbowEnabled, RainbowRoleId, allowed_role_id, RainbowColors
        # 🔒 Permission check
        if not any(r.id == allowed_role_id for r in ctx.author.roles):
            await ctx.send("You don't have permission.")
            return

        role = ctx.guild.get_role(RainbowRoleId)
        if not role:
            await ctx.send("Rainbow role not found.")
            return

        # Avoid duplicates
        if self.running.get(member.id):
            await ctx.send("Rainbow already running for this user.")
            return

        # Give role
        await member.add_roles(role, reason="Rainbow started")

        self.running[member.id] = True
        await ctx.send(f"🌈 Rainbow started for {member.mention}")

        asyncio.create_task(self.rainbow_loop(role, member))

    async def rainbow_loop(self, role, member):
        index = 0

        while self.running.get(member.id, False):
            try:
                await role.edit(color=RainbowColors[index])
                index = (index + 1) % len(RainbowColors)

            except Exception as e:
                print(e)

            await asyncio.sleep(1)

    @commands.command()
    async def stoprainbow(self, ctx, member: commands.MemberConverter):
        global RainbowEnabled, RainbowRoleId, allowed_role_id
        # 🔒 Permission check
        if not any(r.id == allowed_role_id for r in ctx.author.roles):
            return

        role = ctx.guild.get_role(RainbowRoleId)
        if not role:
            return

        # Stop loop
        self.running[member.id] = False

        # Remove role
        try:
            await member.remove_roles(role, reason="Rainbow stopped")
        except Exception as e:
            print(e)

        await ctx.send(f"🌈 Rainbow stopped for {member.mention}")
    
#--------------------Admin---------------#
    @commands.command(name="forceinfect")
    async def force_infect(self, ctx, member: discord.Member):
        if ctx.message.author.id not in developers:
            await ctx.send("You don't have permission to use this command.")
            return
        try:
            if member.bot:
                await ctx.send("❌ Cannot infect bots.")
                return

            data = loads(open('funny.json', 'r').read())

            # Ensure structures exist
            data.setdefault("pinked", [])
            data.setdefault("pink_spread_stats", {})

            # Normalize (VERY important)
            normalized = []
            for u in data["pinked"]:
                if isinstance(u, dict):
                    normalized.append(u)
                else:
                    normalized.append({
                        "id": u,
                        "name": "unknown",
                        "hidden_carrier": False,
                        "infection_stage": 1,
                        "immunity": False
                    })
            data["pinked"] = normalized

            # Check if already infected
            if any(u["id"] == member.id for u in data["pinked"]):
                await ctx.send(f"⚠️ {member.mention} is already infected.")
                return

            # 📊 Stats
            stats = data["pink_spread_stats"]
            stats["forced_infections"] = stats.get("forced_infections", 0) + 1
            stats["total_infections"] = stats.get("total_infections", 0) + 1


            # 🧬 Infect
            await add_to_pinklist(self, member, data, "forced infection")

            # 🎭 Optional: give role immediately
            role = ctx.guild.get_role(1384384321074233434)
            if role and role not in member.roles:
                await member.add_roles(role, reason="Force infected")

            await ctx.send(f"🦠 {member.mention} has been forcefully infected.")

        except Exception as e:
            print(e)
            await ctx.send("❌ Something went wrong.")   
    
#----------Pinkedemic Keyword Utility---------#       
    # ----------------------------
    # 🔍 WORD EXTRACTION
    # ----------------------------
    def extract_words(self, message: str):
        words = re.findall(WORD_REGEX, message.lower())
        return [w for w in words if w not in STOPWORDS]

    # ----------------------------
    # 📉 DECAY
    # ----------------------------
    def decay_word_scores(self, data):
        decay_rate = data.get("keyword_decay_rate", 0.1)

        for word in list(data.get("word_scores", {}).keys()):
            data["word_scores"][word] -= decay_rate

            if data["word_scores"][word] <= 0:
                del data["word_scores"][word]

    # ----------------------------
    # 🔁 PROMOTE WORDS
    # ----------------------------
    def promote_keywords(self, data):
        kw_data = data.setdefault("infection_keywords", {})
        active = kw_data.setdefault("active", [])
        history = kw_data.setdefault("history", [])

        threshold = kw_data.get("threshold", 10)
        max_active = kw_data.get("max_active", 5)

        for word, score in list(data.get("word_scores", {}).items()):
            if score >= threshold and word not in active:
                active.append(word)

        # enforce limit
        while len(active) > max_active:
            removed = active.pop(0)
            history.append(removed)

    # ----------------------------
    # 🧬 UPDATE SCORES
    # ----------------------------
    def update_word_scores(self, data, words, user_entry):
        data.setdefault("word_scores", {})

        weight = 1

        if user_entry:
            if user_entry.get("hidden_carrier"):
                weight = 1.5
            else:
                weight = 2

            stage = user_entry.get("infection_stage", 1)
            weight += (stage * 0.5)

        for word in words:
            data["word_scores"][word] = data["word_scores"].get(word, 0) + weight

    # ----------------------------
    # ☣️ CHECK INFECTION
    # ----------------------------
    async def check_keyword_infection(self, msg, data):
        message = msg.content.lower()
        active_keywords = data.get("infection_keywords", {}).get("active", [])

        for keyword in active_keywords:
            if keyword in message:
                await add_to_pinklist(self, msg.author, None, f"keyword: {keyword}")
                return True

        return False

#------------------Utility---------------#
@staticmethod
async def send_infection_log(self, user,method):
    guild = self.bot.get_guild(1031900634741473280)
    channel = guild.get_channel(1486398908455190590)  # Replace with your log channel ID
    data = loads(open(f'funny.json', 'r').read())
    user_entry = next(
        (u for u in data["pinked"] if u.get("id") == user.id),
        None
    )
    is_carrier = user_entry.get("hidden_carrier", False)
    is_immune = user_entry.get("immunity", False)
    if channel:
        # 🧾 Format message
        carrier_text = " (🧬 Carrier)" if is_carrier else ""
        if is_immune:
            carrier_text += " (🛡️ Immune)"
        await channel.send(
            f"🦠 {user.mention} was infected via **{method}**!{carrier_text}"
        )
        
@staticmethod
async def add_to_pinklist(self, user, data, method):
    """
    Determines if a newly infected user is a hidden carrier based on chance.
    Also adds them to the pinked list with their carrier status.
    """
    if user.id == 974045822167679087:  # Skip if it's the bot itself'
        return
    if data is None:
        data = loads(open(f'funny.json', 'r').read())
    hidden_carrier=False
    guild = self.bot.get_guild(1070759679543750697)
    role = guild.get_role(1384384321074233434)
    vectors = data.get("infection_vectors", {})
    
    # 🔍 Find existing user
    user_entry = next(
        (u for u in data["pinked"]
         if (u["id"] if isinstance(u, dict) else u) == user.id),
        None
    )

    # ----------------------------
    # 🛑 DO NOT RE-INFECT
    # ----------------------------
    if user_entry:
        with open('funny.json', "w") as f:
            dumps(data)
            f.write(dumps(data))
        return  # already infected → do nothing
    
    immunityChance = data.get("immunity_chance", 0.05)        
    immunity = False
    if random.random() < immunityChance and vectors.get("immunity", True):
        immunity = True
        data["pink_spread_stats"]["immune"] = data["pink_spread_stats"].get("immune", 0) + 1
        
    if random.random() < data.get("hidden_carrier_chance", 0.1) and data.get("infection_vectors", {}).get("hidden_carrier", False) and not immunity:
        hidden_carrier = True
        data["pink_spread_stats"]["hidden_carriers"] = data["pink_spread_stats"].get("hidden_carriers", 0) + 1
    else:
        if role and role not in user.roles and not immunity:
            await user.add_roles(role, reason="Pinkedemic (ping infected user)")
    if "pinked" not in data:
        data["pinked"] = []
    # 🔍 Check if user already exists (SAFE)
    exists = any(
        (u.get("id") if isinstance(u, dict) else u) == user.id
        for u in data["pinked"]
    )

    infectionStage = 1
    if immunity:
        infectionStage = 0

    # ➕ Add user
    if not exists:
        data["pinked"].append({
            "id": user.id,
            "name": str(user.name),
            "hidden_carrier": hidden_carrier,
            "infection_stage": infectionStage,
            "immunity": immunity
        })

    # 💾 ALWAYS save
    with open('funny.json', "w") as f:
        dumps(data)
        f.write(dumps(data))
    await send_infection_log(self,user, method)
    
@staticmethod
async def cure_user(self, ctx, user):
    data = loads(open('funny.json', 'r').read())

    # ----------------------------
    # 🔄 GLOBAL CURE RECHARGE
    # ----------------------------
    cure_data = data.setdefault("global_cure", {
        "cure_enabled": True,
        "cure_recharge_enabled": True,
        "current": 5,
        "max": 10,
        "recharge_amount": 1,
        "recharge_interval": 3600,
        "last_recharge": time.time()
    })

    now = time.time()
    
    removeRole=False

    if now - cure_data["last_recharge"] >= cure_data.get("cure_recharge_enabled", True):
        cycles = int((now - cure_data["last_recharge"]) // cure_data["recharge_interval"])

        if cycles > 0 and cure_data["cure_recharge_enabled"]:
            cure_data["current"] = min(
                cure_data["max"],
                cure_data["current"] + (cycles * cure_data["recharge_amount"])
            )
            cure_data["last_recharge"] += cycles * cure_data["recharge_interval"]

    # ----------------------------
    # ❌ NO CURES AVAILABLE
    # ----------------------------
    if cure_data["current"] <= 0:
        await ctx.send("💊 No cures available right now. Try again later.")
        return

    # Consume 1 cure
    cure_data["current"] -= 1

    # ----------------------------
    # ⚙️ SETTINGS
    # ----------------------------
    carrier_chance = data.get("infection", {}).get("cure_to_carrier_chance", 0.2)
    failure_chance = data.get("infection", {}).get("cure_failure_chance", 0.15)

    # ----------------------------
    # 🎲 ROLL OUTCOME
    # ----------------------------
    roll = random.random()

    guild = ctx.guild
    role = guild.get_role(1384384321074233434)

    # ----------------------------
    # 🧬 FAIL → NOTHING HAPPENS
    # ----------------------------
    if roll < failure_chance:
        result = "💀 The cure failed... nothing changed."

    # ----------------------------
    # 🧬 TURN INTO CARRIER
    # ----------------------------
    elif roll < failure_chance + carrier_chance:

        # Remove from infected list
        data["pinked"] = [
            u for u in data.get("pinked", [])
            if u.get("id") != user.id
        ]

        # Add as hidden carrier
        data["pinked"].append({
            "id": user.id,
            "name": str(user.name),
            "hidden_carrier": True,
            "infection_stage": 1,
            "immunity": False
        })

        result = "💊 The cure seemed to work!"
        removeRole=True

    # ----------------------------
    # 💊 SUCCESSFUL CURE
    # ----------------------------
    else:
        removeRole=True
        # Remove from infected list
        data["pinked"] = [
            u for u in data.get("pinked", [])
            if u.get("id") != user.id
        ]
        
        if role and role in user.roles:
            await user.remove_roles(role, reason="Pinkedemic")

        result = "💊 You have cure appears to have worked!"

    # ----------------------------
    # 📊 SAVE DATA (SAFE)
    # ----------------------------
    with open('funny.json', "w") as f:
        f.write(dumps(data, indent=4))

    # Remove role and do it twice because of the re-add loop triggering too fast
    if removeRole and role and role in user.roles:
        await user.remove_roles(role, reason="Pinkedemic cure")
    await asyncio.sleep(1)
    if removeRole and role and role in user.roles:
        await user.remove_roles(role, reason="Pinkedemic cure")
    # ----------------------------
    # 📢 RESPONSE
    # ----------------------------
    await ctx.send(result)  
    
async def setup(bot: commands.Bot):
    await bot.add_cog(FunnyStuff(bot))