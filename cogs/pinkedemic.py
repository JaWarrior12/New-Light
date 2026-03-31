import discord
from discord.ext import commands, tasks
import random, time, json, os, re

from lists import developers

CONFIG_FILE = "Pinkedemic/config.json"
DATA_FILE = "Pinkedemic/data.json"


class InfectionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.evolution_tick.start()

    def cog_unload(self):
        self.evolution_tick.stop()

    # ----------------------------
    # JSON
    # ----------------------------
    def load_json(self, path, default):
        if not os.path.exists(path):
            return default
        with open(path, "r") as f:
            return json.load(f)

    def save_json(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    # ----------------------------
    # INFECTION ENGINE
    # ----------------------------
    async def try_infect(self, user, virus_name, method):
        data = self.load_json(DATA_FILE, {"users": {}, "viruses": {}, "stats": {}})
        config = self.load_json(CONFIG_FILE, {})

        virus = data["viruses"].get(virus_name)
        if not virus:
            return False

        uid = str(user.id)
        entry = data["users"].get(uid)

        if entry and entry.get("infection"):
            return False

        if entry and entry.get("opt_out"):
            return False

        immunity = random.random() < virus.get("immunity_chance", 0.05)
        hidden = False if immunity else random.random() < virus.get("hidden_carrier_chance", 0.1)

        data["users"][uid] = {
            "name": str(user),
            "infection": None if immunity else virus_name,
            "hidden_carrier": hidden,
            "infection_stage": 0 if immunity else 1,
            "immune": immunity
        }

        if not immunity and not hidden:
            role_id = config["infections"][virus_name]["role_id"]
            guild = self.bot.get_guild(config["global"]["guild_id"])
            role = guild.get_role(role_id)
            if role and role not in user.roles:
                await user.add_roles(role)

        stats = data.setdefault("stats", {}).setdefault(virus_name, {})
        stats.setdefault("vector_counts", {})

        if not immunity:
            stats["total_infected"] = stats.get("total_infected", 0) + 1
            stats["vector_counts"][method] = stats["vector_counts"].get(method, 0) + 1
            if not stats.get("patient_zero_time"):
                stats["patient_zero_time"] = time.time()
        else:
            stats["immune"] = stats.get("immune", 0) + 1

        self.save_json(DATA_FILE, data)
        await self.send_infection_log(user, virus_name, method)

        return True

    # ----------------------------
    # KEYWORDS
    # ----------------------------
    async def check_keyword(self, msg, virus_name):
        data = self.load_json(DATA_FILE, {"users": {}, "viruses": {}, "stats": {}})
        config = self.load_json(CONFIG_FILE, {})

        virus = data["viruses"].get(virus_name)
        virus_cfg = config["infections"].get(virus_name)

        if not virus or not virus_cfg:
            return False

        if not virus_cfg["vectors"].get("keyword"):
            return False

        uid = str(msg.author.id)
        entry = data["users"].get(uid)

        if entry and entry.get("infection"):
            return False

        settings = virus_cfg.get("keyword_settings", {})
        keywords = settings.get("hardcoded", []) + virus.get("dynamic_keywords", [])
        blacklist = settings.get("blacklist", [])

        text = msg.content.lower()

        for kw in keywords:
            kw = kw.lower()
            if kw in blacklist:
                continue

            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text):
                return await self.try_infect(msg.author, virus_name, f"keyword:{kw}")

        return False

    # ----------------------------
    # LISTENER
    # ----------------------------
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot or not msg.guild:
            return

        data = self.load_json(DATA_FILE, {"users": {}, "viruses": {}, "stats": {}})
        infected = False

        for virus_name, virus in data["viruses"].items():

            if infected:
                break

            if await self.check_keyword(msg, virus_name):
                infected = True
                continue

            if virus.get("vectors", {}).get("message"):
                if random.random() < virus.get("message_chance", 0.1):
                    if await self.try_infect(msg.author, virus_name, "message"):
                        infected = True
                        continue

    # ----------------------------
    # ROLE RE-ADD
    # ----------------------------
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        data = self.load_json(DATA_FILE, {"users": {}, "viruses": {}, "stats": {}})
        config = self.load_json(CONFIG_FILE, {})

        entry = data["users"].get(str(after.id))
        if not entry:
            return

        virus_name = entry.get("infection")
        if not virus_name:
            return

        if entry.get("hidden_carrier") or entry.get("immune"):
            return

        role_id = config["infections"][virus_name]["role_id"]
        role = after.guild.get_role(role_id)

        if role and role not in after.roles:
            await after.add_roles(role)

    # ----------------------------
    # EVOLUTION
    # ----------------------------
    @tasks.loop(seconds=60)
    async def evolution_tick(self):
        data = self.load_json(DATA_FILE, {"users": {}, "viruses": {}, "stats": {}})
        config = self.load_json(CONFIG_FILE, {})

        now = time.time()

        for virus_name, virus in data.get("viruses", {}).items():
            evo = virus.get("evolution", {})
            if not evo.get("enabled", False):
                continue

            stats = data.setdefault("stats", {}).setdefault(virus_name, {})

            # ------------------------
            # MANUAL OVERRIDE
            # ------------------------
            if evo.get("manual_override", False):
                continue

            mode = evo.get("mode", "schedule")

            # ------------------------
            # SCHEDULE MODE
            # ------------------------
            if mode == "schedule":
                last = virus.get("last_evolution", 0)
                interval = evo.get("schedule", {}).get("time_interval", 600)

                if now - last >= interval:
                    levels = evo.get("schedule", {}).get("levels", [])
                    current = virus.get("current_level", 1)
                    next_level = current + 1

                    for lvl in levels:
                        if lvl["level"] == next_level:
                            virus["vectors"] = {v: True for v in lvl.get("vectors", [])}
                            virus["message_chance"] = lvl.get("infection_chance", virus.get("message_chance", 0.1))
                            virus["current_level"] = next_level
                            virus["last_evolution"] = now

                            await self._announce_evolution(config, virus_name, next_level)
                            break

            # ------------------------
            # RANDOM MODE
            # ------------------------
            elif mode == "random":
                rand_cfg = evo.get("random", {})

                if random.random() < rand_cfg.get("chance", 0.1):
                    available = config.get("vectors", [])
                    max_v = rand_cfg.get("max_vectors", len(available))

                    chosen = random.sample(available, k=random.randint(1, max_v))
                    virus["vectors"] = {v: (v in chosen) for v in available}

                    await self._announce_evolution(config, virus_name, "random")

            # ------------------------
            # INFECTION COUNT EVOLUTION
            # ------------------------
            if evo.get("methods", {}).get("infection_count", False):
                thresholds = evo.get("schedule", {}).get("infection_thresholds", [])
                total = stats.get("total_infected", 0)

                for i, threshold in enumerate(thresholds):
                    target_level = i + 1
                    if total >= threshold and virus.get("current_level", 1) < target_level:

                        levels = evo.get("schedule", {}).get("levels", [])
                        for lvl in levels:
                            if lvl["level"] == target_level:
                                virus["vectors"] = {v: True for v in lvl.get("vectors", [])}
                                virus["current_level"] = target_level
                                virus["last_evolution"] = now

                                await self._announce_evolution(config, virus_name, target_level)
                                break

        self.save_json(DATA_FILE, data)

    # ----------------------------
    # COMMANDS
    # ----------------------------

    @commands.command()
    async def force_infect(self, ctx, user: discord.Member, virus_name: str):
        if ctx.author.id not in developers:
            return
        await self.try_infect(user, virus_name, "force")
        await ctx.send(f"{user} infected.")

    @commands.command()
    async def start_infection(self, ctx, virus_name: str, member: discord.Member = None):
        if ctx.author.id not in developers:
            return

        config = self.load_json(CONFIG_FILE, {})
        guild = self.bot.get_guild(config["global"]["guild_id"])

        if not member:
            role = guild.get_role(config["global"]["initial_infection_role"])
            pool = [m for m in guild.members if not m.bot and (role in m.roles if role else True)]
            if not pool:
                await ctx.send("No valid members.")
                return
            member = random.choice(pool)

        await self.try_infect(member, virus_name, "initial")
        await ctx.send(f"{member} infected.")

    @commands.command()
    async def cure_user(self, ctx, user: discord.Member):
        data = self.load_json(DATA_FILE, {"users": {}, "viruses": {}, "stats": {}})
        config = self.load_json(CONFIG_FILE, {})

        entry = data["users"].get(str(user.id))
        if not entry or not entry.get("infection"):
            return

        virus_name = entry["infection"]
        role_id = config["infections"][virus_name]["role_id"]
        role = ctx.guild.get_role(role_id)

        if role and role in user.roles:
            await user.remove_roles(role)

        entry["infection"] = None
        entry["hidden_carrier"] = False
        entry["infection_stage"] = 0

        self.save_json(DATA_FILE, data)

    @commands.command()
    async def cure_all(self, ctx):
        if ctx.author.id not in developers:
            return

        data = self.load_json(DATA_FILE, {"users": {}, "viruses": {}, "stats": {}})
        config = self.load_json(CONFIG_FILE, {})

        guild = self.bot.get_guild(config["global"]["guild_id"])

        for uid, entry in data["users"].items():
            if entry.get("infection"):
                role_id = config["infections"][entry["infection"]]["role_id"]
                member = guild.get_member(int(uid))
                role = guild.get_role(role_id)
                if member and role and role in member.roles:
                    await member.remove_roles(role)

                entry["infection"] = None

        self.save_json(DATA_FILE, data)

    @commands.command()
    async def stats(self, ctx, virus_name):
        data = self.load_json(DATA_FILE, {"users": {}, "viruses": {}, "stats": {}})

        stats = data["stats"].get(virus_name, {})
        p0 = stats.get("patient_zero_time")

        if p0:
            elapsed = int(time.time() - p0)
            time_str = str(time.timedelta(seconds=elapsed))
        else:
            time_str = "N/A"

        current = sum(1 for u in data["users"].values() if u.get("infection") == virus_name)

        await ctx.send(f"{virus_name} | Time since P0: {time_str} | Infected: {current}")

    # ----------------------------
    # LOGGING
    # ----------------------------
    async def send_infection_log(self, user, virus_name, method):
        guild = self.bot.get_guild(1031900634741473280)
        channel = guild.get_channel(1486398908455190590)
        if channel:
            await channel.send(f"🦠 {user} infected with {virus_name} via {method}")


async def setup(bot):
    await bot.add_cog(InfectionCog(bot))