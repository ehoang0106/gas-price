import discord
from discord.ext import commands
from dotenv import dotenv_values
import requests
from gas_price import search_gas_prices


config = dotenv_values(".env")
TOKEN = config['DISCORD_TOKEN']
PREFIX = "+"


bot = discord.Client()
bot = commands.Bot(command_prefix=PREFIX)

#setup gihub api
#this setup is to trigger the github action to run the gas price search
GITHUB_TOKEN = config['GITHUB_TOKEN']
OWNER = 'ehoang0106'
REPO = 'gas-price'
WORKFLOW_ID = 'workflow.yml'
url = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/dispatches'
headers = { 'Authorization': f'token {GITHUB_TOKEN}' }
payload = { 'ref': 'master' }

#end setup github api


@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="gas prices"))

@bot.command(name="gas")
async def gas(ctx, *, location): # * is get all the arguments after the command
  await ctx.send(f"I'm searching for gas prices in {location}.\n Please wait a moment...")
  
  #call api to trigger the github action
  response = requests.post(url, headers=headers, json=payload)
  
  if response.status_code == 204:
    gas_prices = search_gas_prices(location)
    if gas_prices:
        print('Results: ')
        for station in gas_prices:
          print(station)
          await ctx.send(f"```---------------\nStation Name: {station['station_name']}\nPrice: {station['price']}\nAddress: {station['address']}\n```\n{station['map_url']}\n")
    else:
      await ctx.send("An error occurred while searching for gas prices.")
  
  
bot.run(TOKEN)