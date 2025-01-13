
import discord
from discord.ext import commands, tasks
from dotenv import dotenv_values
import requests
from main import search_gas_prices
import time
from datetime import datetime

config = dotenv_values(".env")
TOKEN = config['DISCORD_TOKEN']
PREFIX = "+"
CHANNEL_ID = config['DISCORD_CHANNEL_ID'] 

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="gas prices"))


@tasks.loop(hours=24)  
async def send_gas_prices():
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel:
        current_time = datetime.now().strftime("%m/%d/%Y, %I:%M %p")
        await channel.send(f"`Date`: `{current_time}`")
        await channel.send(f"I'm searching for gas prices.\nPlease wait a moment...\n")
        await search_and_send_gas_prices(channel, "Garden Grove")

@bot.command(name="start")
async def start(ctx): 
    send_gas_prices.start()
    await ctx.send("Gas price search has started.")

@bot.command(name="stop")
async def stop(ctx):
    send_gas_prices.stop()
    await ctx.send("Gas price search has stopped.")

@bot.command(name="gas")
async def gas(ctx, *, location):
    await ctx.send(f"Date: {time.ctime()}")                                      
    await ctx.send(f"I'm searching for gas prices.\nPlease wait a moment...\n")
    await search_and_send_gas_prices(ctx, location)

async def search_and_send_gas_prices(destination, location):
    gas_prices, lowest_price_station = search_gas_prices(location)
    
    if gas_prices:
        await destination.send("\n**Found :three: Gas Stations near you: **\n")
        for station in gas_prices:
            await destination.send(f"```---------------\n⛽ Station Name: {station['station_name']}\n💵 Price: {station['price']}\n🗺️ Address: {station['address']}\n```")
    else:
        await destination.send("An error occurred while searching for gas prices.")
    
    if lowest_price_station:
        await destination.send("\n-----------------------------------\n")
        await destination.send("\n**✅ Here is the Gas Station with the lowest price: **\n")
        await destination.send(f"```---------------\n⛽ Station Name: {lowest_price_station['station_name']}\n💵 Price: {lowest_price_station['price']}\n🗺️ Address: {lowest_price_station['address']}\n```")
    else:
        await destination.send("An error occurred while searching for the lowest price gas station.")

bot.run(TOKEN)