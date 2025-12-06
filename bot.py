import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Read token and channel ID from environment variables
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # convert string to int

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    scheduler.start()

    # Schedule messages starting 5:05 AM, one per minute
    scheduler.add_job(send_checkin, "cron", hour=5, minute=5)
    scheduler.add_job(send_opening, "cron", hour=5, minute=6)
    scheduler.add_job(send_giveaway, "cron", hour=5, minute=7)

async def send_checkin():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(
            "💻 **CHECK-IN** 💻\n\n"
            "Good morning! Don’t forget that check-in starts at **9:00**! "
            "You'll receive a welcome pack that includes the badge, where you have the schedule of the event. "
            "Please arrive on time to avoid large crowds ☕"
        )

async def send_opening():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(
            "⚡ **Official opening** ⚡\n\n"
            "The official opening starts in **30 minutes** and it will take place in **AN010**. "
            "Our partners will present their companies, and it’s a good opportunity to ask questions and network 💥\n\n"
            "Then, our main sponsor, **HazelHeartwood**, will tell you everything you need to know about the main challenge, "
            "so make sure to be on time ⌚"
        )

async def send_giveaway():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(
            "🎁 **Giveaway** 🎁\n\n"
            "The giveaway started! To participate, you have to fulfill the following requirements:\n\n"
            "💥 Follow **@bestem.bucharest**\n"
            "⚡ Follow **@cyberjump_bucuresti**\n"
            "🤳 Post a story and tag **@bestem.bucharest**\n\n"
            "We have exciting prizes for the winners, so make sure to do it before **18:00**!"
        )

bot.run(TOKEN)
