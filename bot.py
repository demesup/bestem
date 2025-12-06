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

    # Schedule all messages according to the new timetable
    scheduler.add_job(send_checkin, "cron", hour=8, minute=0, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_opening, "cron", hour=9, minute=30, timezone=BUCHAREST_TZ)
    
    scheduler.add_job(send_giveaway_start, "cron", hour=13, minute=0, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_fun_activities, "cron", hour=14, minute=0, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_lunch, "cron", hour=15, minute=0, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_giveaway_end, "cron", hour=17, minute=30, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_dinner, "cron", hour=20, minute=0, timezone=BUCHAREST_TZ)
    scheduler.add_job(send_maze_game, "cron", hour=22, minute=45, timezone=BUCHAREST_TZ)

    scheduler.start()
    print("Scheduler started.")

async def send_checkin():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "💻CHECK-IN💻@everyone\n\n"
        "Good morning! Don’t forget that check-in starts at 9:00! "
        "You'll receive a welcome pack that includes the badge, where you have the schedule of the event. "
        "Please arrive on time to avoid large crowds ☕"
    )

async def send_opening():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "⚡Official opening⚡@everyone\n\n"
        "The official opening starts in 30 minutes and it will take place in AN010. "
        "Our partners will present their companies, and it’s a good opportunity to ask questions and network 💥\n\n"
        "Then, our main sponsor, HazelHeartwood, will tell you everything you need to know about the main challenge, "
        "so make sure to be on time ⌚"
    )


async def send_fun_activities():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "✨ FUN ACTIVITIES ✨ @everyone\n\n"
        "If you ever get tired of coding, there are several fun activities scattered around the hallway:\n\n"
        "🔥 BURN CORNER - rest and recharge.\n"
        "🍿 ARCANE CORNER - watch Arcane with snacks.\n"
        "🖼 MEME WALL - get creative and share jokes!\n"
        "💻 Partners’ Booths - explore exciting activities.\n\n"
        "💥 More activities will be available later, but enjoy these for now!"
    )

async def send_lunch():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "🍕 Lunch 🍕 @everyone\n\n"
        "Lunch is ready! You can pick it up from the designated area until 16:00. "
        "Please come to collect it as soon as possible to avoid long queues!\n\n"
        "If you have any dietary preferences (such as vegetarian), you can communicate them to the volunteers 🙂"
    )

async def send_giveaway_start():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "🎁 Giveaway 🎁 @everyone\n\n"
        "The giveaway started! To participate, you have to fulfill the following requirements:\n\n"
        "💥 Follow @bestem.bucharest\n"
        "⚡ Follow @mindarchitect.ro\n"
        "🤳 Post a story and tag @bestem.bucharest\n\n"
        "We have exciting prizes for the winners, so make sure to do it before 18:00!"
    )

async def send_giveaway_end():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "🎁 Giveaway 🎁 @everyone\n\n"
        "The giveaway is almost over! You have 30 minutes left to complete the requirements:\n\n"
        "💥 Follow @bestem.bucharest\n"
        "⚡ Follow @mindarchitect.ro\n"
        "🤳 Post a story and tag @bestem.bucharest\n\n"
        "🎁 Don’t miss out on your chance to win exciting prizes! Good luck!"
    )

async def send_dinner():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "🥪 Dinner 🥪 @everyone\n\n"
        "Dinner is ready! The volunteers will bring it to you so you don't have to hurry 🍽\n\n"
        "If you have any dietary preferences (such as vegetarian), you can communicate them to the volunteers 🙂"
    )

async def send_maze_game():
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        "🎲 Maze Game 🎲 @everyone\n\n"
        "If you still have some energy, we have prepared a fun activity that will test your problem-solving skills and teamwork 🤝\n\n"
        "⚡ Gather your team in the designated area, or join alone and enjoy the fun! "
        "If you have trouble finding it, ask a volunteer for help!"
    )

bot.run(TOKEN)
