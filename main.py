# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

#self-made packages
from keep_alive import keep_alive
from adfunc import read_data, write_data

load_dotenv()
bot = commands.Bot(command_prefix='$')

#initialization
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')
channel_id = os.getenv('CHANNEL_ID')
admin_channel = os.getenv('ADMIN_CHANNEL')
logs_channel = os.getenv('LOGS_CHANNEL')
command_execute = 0
ts_lastshroom = 0
shroom_count = 0
last_farmer = 0
last_mushroom = 0

  
@bot.event
async def on_ready(): #bot boots up
  print(f'{bot.user.name} has connected to Discord')

@bot.listen('on_message') #waits for the on_message() event to be called
async def shroom_farm(message):
  global shroom_count
  global last_farmer
  global last_mushroom
  global ts_lastshroom
  if str(message.channel.id) in channel_id and not message.author.bot:
    if message.author.id != last_farmer:
      if message.content == '🍄':
        current_dt = datetime.now().strftime('%d')
        print(current_dt)
        if current_dt != ts_lastshroom:
          last_farmer = 0
          shroom_count = 0
          ts_lastshroom = current_dt
          reset_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
          channel_to_send = int(logs_channel)
          channel = bot.get_channel(channel_to_send)
          await channel.send(f'Count reset at {reset_time}')
        if message.author.id != last_farmer:
          last_mushroom = current_dt
          shroom_count += 1
          last_farmer = message.author.id
          if shroom_count == 1:
            await message.channel.send('First mushroom farmed today!🍄')
          else:
            await message.channel.send(f'{shroom_count} mushrooms farmed today!🍄')  
    else:
      await message.channel.send('You can only farm 1 mushroom at a time')


@bot.command(name='save_count', brief='Saves the current count', description='Saves the current count to the database (Requires administrator access) - WIP')
async def save_count(message):
  current_dt = 0
  current_ts = 0
  if message.author.id == int(OWNER_ID) and not message.guild:
    current_dt = datetime.now()
    current_ts = datetime.timestamp(current_dt)
    write_data(shroom_count, current_ts)
    print('Count saved')
    await message.channel.send('Count saved')
    command_execution = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    channel_to_send = int(logs_channel)
    channel = bot.get_channel(channel_to_send)
    await channel.send(f'save_count command executed at {command_execution}')
  else:
    await message.channel.send('You do not have sufficient permissions to use this command')
  
@bot.command(name='show_save', brief='Shows the current save', description='Shows the current save')
async def show_save(message):
  current_json = read_data()
  await message.channel.send(current_json)
  command_execution = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
  channel_to_send = int(logs_channel)
  channel = bot.get_channel(channel_to_send)
  await channel.send(f'show_count command executed at {command_execution}')

@bot.command(name='edit_count', brief='Changes the current count', description='Changes the current count (Requires administrator access)')
async def edit_count(message, new_count):
  global shroom_count
  if message.author.id == int(OWNER_ID) and not message.guild:
    shroom_count = int(new_count)
    await message.channel.send(f'Count changed to {new_count}')
    command_execution = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    channel_to_send = int(logs_channel)
    channel = bot.get_channel(channel_to_send)
    await channel.send(f'edit_count command executed at {command_execution}')
  else:
    await message.channel.send('You do not have sufficient permissions to use this command')

@bot.command(name='dev_warning', brief='Sends a dev warning', description='Sends a warning about active development to the target channel (Requires administrator access)')
async def dev_warning(message, target_channel):
  if message.author.id == int(OWNER_ID) and not message.guild: #checks if the person sending the command has permissions to do so, and if its in a DM channel
    channel_to_send = int(target_channel)
    channel = bot.get_channel(channel_to_send)
    await channel.send('This bot is currently under maintenance')

@bot.command(name='send', brief='Sends a message as the bot', description='Sends a message to the target channel as the bot (Requires administrator access)')
async def remote_send(message, target_channel, *, arg):
  if message.author.id == int(OWNER_ID) and not message.guild: #checks if the person sending the command has permissions to do so, and if its in a DM channel
    channel_to_send = int(target_channel)
    channel = bot.get_channel(channel_to_send)
    await channel.send(arg)
    command_execution = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    channel_to_send = int(logs_channel)
    channel = bot.get_channel(channel_to_send)
    await channel.send(f'remote_send command executed at {command_execution}')

keep_alive()
bot.run(TOKEN)