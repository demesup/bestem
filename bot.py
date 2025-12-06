import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

# Read token and channel ID from environment variables
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    raise ValueError("TOKEN and CHANNEL_ID must be set in environment variables!")

CHANNEL_ID = int(CHANNEL_ID)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

# Timezone for Bucharest
BUCHAREST_TZ = timezone("Europe/Bucharest")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # DAY 2 — Only the two remaining messages
    scheduler.add_job(send_speed_typing, "cron", hour=2, minute=0, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_breakfast, "cron", hour=8, minute=0, timezone=BUCHAREST_TZ)

    scheduler.start()
    print("Scheduler started.")


# -----------------------
# DAY 2 MESSAGE FUNCTIONS
# -----------------------

async def send_speed_typing():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "💻 Speed typing 💻 @everyone\n\n"
        "Are you still awake? Test your typing skills for a chance to win a prize 🎁\n\n"
        "The activity will take place between 02:00 and 02:30, so make sure you come on time!"
    )


async def send_breakfast():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "🍲 Breakfast 🍲 @everyone\n\n"
        "Breakfast is ready! The volunteers will bring it to you so you don't have to hurry or leave the table 🥫\n\n"
        "If you have any dietary preferences (such as vegetarian), tell the volunteers and they'll serve you accordingly 🙂"
    )


bot.run(TOKEN)
