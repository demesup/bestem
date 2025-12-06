import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

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

BUCHAREST_TZ = timezone("Europe/Bucharest")

# List of messages with a friendly name
messages = [
    ("💻CHECK-IN💻@everyone\n\nGood morning! Don’t forget that check-in starts at 9:00! You'll receive a welcome pack that includes the badge, where you have the schedule of the event. Please arrive on time to avoid large crowds ☕", "Check-in"),
    ("⚡Official opening⚡@everyone\n\nThe official opening starts in 30 minutes and it will take place in AN010. Our partners will present their companies, and it’s a good opportunity to ask questions and network 💥\n\nThen, our main sponsor, HazelHeartwood, will tell you everything you need to know about the main challenge, so make sure to be on time ⌚", "Opening"),
    ("🎁 Giveaway 🎁@everyone\n\nThe giveaway started! To participate, you have to fulfill the following requirements:\n\n💥 Follow @bestem.bucharest\n⚡ Follow @cyberjump_bucuresti\n🤳 Post a story and tag @bestem.bucharest\n\nWe have exciting prizes for the winners, so make sure to do it before 18:00!", "Giveaway Start"),
    ("✨ FUN ACTIVITIES ✨ @everyone\n\nIf you ever get tired of coding, there are several fun activities scattered around the hallway:\n\n🔥 BURN CORNER - rest and recharge.\n🍿 ARCANE CORNER - watch Arcane with snacks.\n🖼 MEME WALL - get creative and share jokes!\n💻 Partners’ Booths - explore exciting activities.\n\n💥 More activities will be available later, but enjoy these for now!", "Fun Activities"),
    ("🍕 Lunch 🍕 @everyone\n\nLunch is ready! You can pick it up from the designated area until 16:00. Please come to collect it as soon as possible to avoid long queues!\n\nIf you have any dietary preferences (such as vegetarian), you can communicate them to the volunteers 🙂", "Lunch"),
    ("🎁 Giveaway 🎁 @everyone\n\nThe giveaway is almost over! You have 30 minutes left to complete the requirements:\n\n💥 Follow @bestem.bucharest\n⚡ Follow @cyberjump_bucuresti\n🤳 Post a story and tag @bestem.bucharest\n\n🎁 Don’t miss out on your chance to win exciting prizes! Good luck!", "Giveaway End"),
    ("🥪 Dinner 🥪 @everyone\n\nDinner is ready! The volunteers will bring it to you so you don't have to hurry 🍽\n\nIf you have any dietary preferences (such as vegetarian), you can communicate them to the volunteers 🙂", "Dinner"),
    ("🎲 Maze Game 🎲 @everyone\n\nIf you still have some energy, we have prepared a fun activity that will test your problem-solving skills and teamwork 🤝\n\n⚡ Gather your team in the designated area, or join alone and enjoy the fun! If you have trouble finding it, ask a volunteer for help!", "Maze Game")
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Schedule messages with 1-minute intervals starting at 07:20
    start_hour = 7
    start_minute = 20
    for i, (message, name) in enumerate(messages):
        scheduler.add_job(
            send_message, 
            "cron",
            hour=start_hour,
            minute=start_minute + i,
            args=[message, name],
            timezone=BUCHAREST_TZ
        )

    scheduler.start()
    print("Test scheduler started.")

async def send_message(message, name):
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(message)
    print(f"Sent '{name}' message.")

bot.run(TOKEN)
