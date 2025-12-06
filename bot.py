import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

# Read token and channel ID from environment variables
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Ensure environment variables exist
if not TOKEN or not CHANNEL_ID:
    raise ValueError("TOKEN and CHANNEL_ID must be set in environment variables!")

CHANNEL_ID = int(CHANNEL_ID)  # Convert string to int

# Intents setup: minimal required for sending to private channels
intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Needed for role-based private channels

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

# Timezone for Bucharest
BUCHAREST_TZ = timezone("Europe/Bucharest")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Schedule messages at 5:40, 5:41, 5:42 Bucharest time
    scheduler.add_job(send_checkin, "cron", hour=5, minute=40, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_opening, "cron", hour=5, minute=41, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_giveaway, "cron", hour=5, minute=42, timezone=BUCHAREST_TZ)

    scheduler.start()
    print("Scheduler started.")

async def send_checkin():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "💻 **CHECK-IN** 💻\n\n"
        "Good morning! Don’t forget that check-in starts at **9:00**! "
        "You'll receive a welcome pack that includes the badge, where you have the schedule of the event. "
        "Please arrive on time to avoid large crowds ☕"
    )

async def send_opening():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "⚡ **Official opening** ⚡\n\n"
        "The official opening starts in **30 minutes** and it will take place in **AN010**. "
        "Our partners will present their companies, and it’s a good opportunity to ask questions and network 💥\n\n"
        "Then, our main sponsor, **HazelHeartwood**, will tell you everything you need to know about the main challenge, "
        "so make sure to be on time ⌚"
    )

async def send_giveaway():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "🎁 **Giveaway** 🎁\n\n"
        "The giveaway started! To participate, you have to fulfill the following requirements:\n\n"
        "💥 Follow **@bestem.bucharest**\n"
        "⚡ Follow **@cyberjump_bucuresti**\n"
        "🤳 Post a story and tag **@bestem.bucharest**\n\n"
        "We have exciting prizes for the winners, so make sure to do it before **18:00**!"
    )

bot.run(TOKEN)
