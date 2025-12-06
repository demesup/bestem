import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = YOUR_CHANNEL_ID  # int

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    scheduler.start()

    # Schedule starting 16:40 every minute for testing
    scheduler.add_job(send_checkin, "cron", hour=16, minute="40-42")  # 16:40, 16:41, 16:42
    scheduler.add_job(send_opening, "cron", hour=16, minute="43-45")  # 16:43, 16:44, 16:45
    scheduler.add_job(send_giveaway, "cron", hour=16, minute="46-48")  # 16:46, 16:47, 16:48

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
