# bot.py
import os
import discord
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
  global embed
  global shroom_count
  global last_farmer
  global last_mushroom
  global ts_lastshroom
  if message.content == '🍄':
    if message.author.id != last_farmer:
      if str(message.channel.id) in channel_id: #and not message.author.bot:
        current_dt = datetime.now().strftime('%d')
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
            embed = discord.Embed(title="Mushroom Farmed!", description="First mushroom farmed today!🍄", color=discord.Color.red())
            await message.channel.send(embed=embed)
            
          else:
            embed = discord.Embed(title="Mushroom Farmed!", description=f"{shroom_count} mushrooms farmed today!🍄", color=discord.Color.red())
            await message.channel.send(embed=embed)
          farm_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") 
          write_data(shroom_count, farm_time)
    else:
      embed = discord.Embed(title="You cannot farm mushrooms now", description="You can only farm one mushroom at a time", color=discord.Color.red())
      await message.channel.send(embed=embed)
  
  

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
    embed = discord.Embed(title="Dev warning", description="The bot will currently be under development")
    await channel.send(embed=embed)
    #await channel.send("This bot is currently under maintenance")

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

@bot.command(name='test_embed')
async def test_embed(message):
  if message.author.id == int(OWNER_ID):
    embed = discord.Embed(title="Yes but No", description="Yes, but no, but yes but no, but actually yes, but legitamately no, while yes else no but yes but no but oui but nein but yes yes no no yes no no yes no no yes no no yes and no but yes but no but yes but Flag: {yes, but no} yes but no no no no no no no and yes but no but no", color=discord.Color.blue())
    await message.channel.send(embed=embed)

keep_alive()
bot.run(TOKEN)