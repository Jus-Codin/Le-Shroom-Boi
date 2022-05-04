# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

#self-made packages
from keep_alive import keep_alive
from datadump import read_data, write_data

#initialization
load_dotenv()
current_dt = 0
current_ts = 0
TOKEN = os.getenv('DISCORD_TOKEN')
channel_id = [958289601263468554, 970627902389518377]
shroom_count = 0
#client = discord.Client()
bot = commands.Bot(command_prefix='$')
last_farmer = 0
  
@bot.event
async def on_ready(): #bot boots up
  print(f'{bot.user.name} has connected to Discord')

@bot.command(name='farm')
async def shroom_farm(message):
  global shroom_count
  global last_farmer
  if message.channel.id in channel_id and not message.author.bot:
    if message.author.id != last_farmer:
      if message.content.contains('🍄'): # mushroom farming trigger
        shroom_count += 1
        last_farmer = message.author.id
        if shroom_count == 1:
          await message.channel.send('First mushroom farmed today!🍄')
        else:
          await message.channel.send(f'{shroom_count} mushrooms farmed today!🍄')

    else:
      await message.content.send('You can only farm 1 mushroom at a time')


@bot.command(name='save_count')
async def save_count(message):
  global current_dt
  global current_ts
  current_dt = datetime.now()
  current_ts = datetime.timestamp(current_dt)
  write_data(shroom_count, current_ts)
  await message.channel.send('Count saved')
  
@bot.command(name='show_save')
async def show_save(message):
  current_json = read_data()
  await message.channel.send(current_json)


keep_alive()
bot.run(TOKEN)
