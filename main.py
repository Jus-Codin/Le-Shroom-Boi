# bot.py
import os
import pytz
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from adfunc import write_data, read_data

#self-made packages
#from keep_alive import keep_alive

load_dotenv()
bot = commands.Bot(command_prefix='$')

#initialization
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')
channel_id = os.getenv('CHANNEL_ID')
admin_channel = os.getenv('ADMIN_CHANNEL')
logs_channel = os.getenv('LOGS_CHANNEL')
sgt = pytz.timezone('Asia/Singapore')
command_execute = 0
ts_lastshroom = 0
shroom_count = 0
last_farmer = 0
last_mushroom = 0

  
@bot.event
async def on_ready(): #bot boots up
  #global shroom_count
  #startup_timestamp = datetime.now(sgt).strftime('%Y/%m/%d, %H:%M:%S')
  #shroom_count = crash_check(shroom_count, startup_timestamp)
  print(f'{bot.user.name} has connected to Discord')

@bot.listen('on_message') #waits for the on_message() event to be called
async def shroom_farm(message):
  global embed
  global shroom_count
  global last_farmer
  global last_mushroom
  global ts_lastshroom
  origin_id = 0
  if message.content == '🍄':
    if message.author.id != last_farmer:
      if str(message.channel.id) in channel_id and not message.author.bot:
        current_dt = datetime.now(sgt).strftime('%d')
        if current_dt != ts_lastshroom:
          last_farmer = 0
          shroom_count = 0
          ts_lastshroom = current_dt
          reset_time = datetime.now(sgt).strftime('%Y/%m/%d, %H:%M:%S')
          channel_to_send = int(logs_channel)
          channel = bot.get_channel(channel_to_send)
          command_embed = discord.Embed(title="Count resetted", description=f'Count resetted at {reset_time}', color=discord.Color.red())
          await channel.send(embed=command_embed)
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
          farm_time = datetime.now(sgt).strftime('%Y/%m/%d %H:%M:%S')
          origin_id = message.guild.id
          write_data(shroom_count, farm_time, origin_id)
    else:
      embed = discord.Embed(title="You cannot farm mushrooms now", description="You can only farm one mushroom at a time", color=discord.Color.green())
      await message.channel.send(embed=embed)

@bot.command(name='edit_count', brief='Changes the current count', description='Changes the current count (Requires administrator access)')
async def edit_count(message, new_count):
  global shroom_count
  if message.author.id == int(OWNER_ID) and not message.guild:
    last_count = shroom_count
    shroom_count = int(new_count)
    await message.channel.send(f'Count changed to {new_count}')
    command_execution = datetime.now(sgt).strftime('%Y/%m/%d, %H:%M:%S')
    channel_to_send = int(logs_channel)
    channel = bot.get_channel(channel_to_send)
    command_embed = discord.Embed(title="edit_count command executed", description=f'Count changed to {command_execution}', color=discord.Color.green())
    farm_time = datetime.now(sgt).strftime('%Y/%m/%d %H:%M:%S')
    origin_id = message.guild.id
    write_data(shroom_count, farm_time, origin_id)
    command_embed.add_field(name='Count changed from:', value=last_count)
    command_embed.add_field(name='New count:', value=new_count)
    await channel.send(embed=command_embed)
  else:
    await message.channel.send('You do not have sufficient permissions to use this command')

@bot.command(name='dev_warning', brief='Sends a dev warning', description='Sends a warning about active development to the target channel (Requires administrator access)')
async def dev_warning(message, target_channel):
  if message.author.id == int(OWNER_ID) and not message.guild: #checks if the person sending the command has permissions to do so, and if its in a DM channel
    channel_to_send = int(target_channel)
    channel = bot.get_channel(channel_to_send)
    embed = discord.Embed(title="Dev warning", description="The bot will currently be under development")
    await channel.send(embed=embed)

@bot.command(name='send', brief='Sends a message as the bot', description='Sends a message to the target channel as the bot (Requires administrator access)')
async def remote_send(message, target_channel, *, arg):
  if message.author.id == int(OWNER_ID) and not message.guild: #checks if the person sending the command has permissions to do so, and if its in a DM channel
    channel_to_send = int(target_channel)
    channel = bot.get_channel(channel_to_send)
    await channel.send(arg)
    command_execution = datetime.now(sgt).strftime('%Y/%m/%d, %H:%M:%S')
    channel_to_send = int(logs_channel)
    channel = bot.get_channel(channel_to_send)
    command_embed = discord.Embed(title="remote_send command executed", description=f'Command executed at {command_execution}', color=discord.Color.green())
    command_embed.add_field(name="Message sent:", value=arg)
    command_embed.add_field(name="Message sent to:", value=str(target_channel))
    await channel.send(embed=command_embed)

@bot.command(name='show_save')
async def showsave(message):
  if message.author.id == int(OWNER_ID):
    current_save = read_data()
    await message.channel.send(current_save)

@bot.event
async def on_command_error(message, errormsg):
  if isinstance(errormsg, commands.CommandNotFound):
    command_embed = discord.Embed(title='Invalid Command', description='Command does not exist', color=discord.Color.red())
    await message.channel.send(embed=command_embed)
    error_caught_timestamp =  datetime.now(sgt).strftime('%Y/%m/%d, %H:%M:%S')
    channel_to_send = int(logs_channel)
    channel = bot.get_channel(channel_to_send)
    error_embed = discord.Embed(title="Invalid command detected", description='A user has tried to execute an invalid command', color=discord.Color.red())
    error_embed.add_field(name="Invalid command:", value=message)
    error_embed.add_field(name="Error message:", value=errormsg)
    error_embed.add_field(name="Timestamp error generated:", value=error_caught_timestamp)
    await channel.send(embed=error_embed)
    

#keep_alive()
bot.run(TOKEN)