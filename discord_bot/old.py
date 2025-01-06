#old code

import discord
from discord.ext import commands
from dotenv import dotenv_values
import requests
#from gas_price import search_gas_prices
from main import search_gas_prices
import time

config = dotenv_values(".env")
TOKEN = config['DISCORD_TOKEN']
PREFIX = "+"


bot = discord.Client()
bot = commands.Bot(command_prefix=PREFIX)

#setup gihub api
#this setup is to trigger the github action to run the gas price search

# GITHUB_TOKEN = config['GITHUB_TOKEN']
# OWNER = 'ehoang0106'
# REPO = 'gas-price'
# WORKFLOW_ID = 'workflow.yml'
# url = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/dispatches'
# headers = { 'Authorization': f'token {GITHUB_TOKEN}' }
# payload = { 'ref': 'master' }

#end setup github api


# @bot.event
# async def on_ready():
#   print(f'{bot.user} has connected to Discord!')
#   await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="gas prices"))
  

# @bot.command(name="gas")
# async def gas(ctx, *, location): # * is get all the arguments after the command
#   await ctx.send(f"I'm searching for gas prices.\nPlease wait a moment...\n")
  
#   #call api to trigger the github action
#   #response = requests.post(url, headers=headers, json=payload)
  
#   #if response.status_code == 204:
#   gas_prices, lowest_price_station = search_gas_prices(location)
  
#   if gas_prices:
#       print('Results: ')
#       await ctx.send("\n**Found :three: Gas Stations near you: **\n")
#       for station in gas_prices:
#         print(station)
#         await ctx.send(f"```---------------\n⛽ Station Name: {station['station_name']}\n💵 Price: {station['price']}\n🗺️ Address: {station['address']}\n```")
        
#   else:
#     await ctx.send("An error occurred while searching for gas prices.")
    
#   if lowest_price_station:
#     await ctx.send("\n-----------------------------------\n")
#     await ctx.send("\n**✅ Here is the Gas Station with the lowest price: **\n")
#     await ctx.send(f"```---------------\n⛽ Station Name: {lowest_price_station['station_name']}\n💵 Price: {lowest_price_station['price']}\n🗺️ Address: {lowest_price_station['address']}\n```")
#   else:
#       await ctx.send("An error occurred while searching for the lowest price gas station.")
  
# bot.run(TOKEN)