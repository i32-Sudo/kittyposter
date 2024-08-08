import discord
import aiohttp
import asyncio
from discord.ext import commands

# Replace with your bot's token
TOKEN = 'O_O'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

friend_user_id = None
interval = None
task = None

async def fetch_cat_picture():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.thecatapi.com/v1/images/search') as response:
            if response.status == 200:
                data = await response.json()
                return data[0]['url']
            else:
                return None

async def send_cat_pictures(ctx):
    global friend_user_id, interval, task
    friend = await bot.fetch_user(friend_user_id)
    while not bot.is_closed():
        cat_picture_url = await fetch_cat_picture()
        if cat_picture_url:
            await friend.send(cat_picture_url)
        await asyncio.sleep(interval)  # Wait for the specified interval before sending the next picture

@bot.command(name='start')
async def start(ctx, user_id: int, time_interval: float):
    global friend_user_id, interval, task
    friend_user_id = user_id
    interval = time_interval
    if task is None or task.done():
        task = bot.loop.create_task(send_cat_pictures(ctx))
        await ctx.send(f'Started sending cat pictures to {friend_user_id} every {interval} seconds.')
    else:
        await ctx.send('Cat picture sending is already running.')

@bot.command(name='stop')
async def stop(ctx):
    global task
    if task is not None and not task.done():
        task.cancel()
        task = None
        await ctx.send('Stopped sending cat pictures.')
    else:
        await ctx.send('Cat picture sending is not running.')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

bot.run(TOKEN)
