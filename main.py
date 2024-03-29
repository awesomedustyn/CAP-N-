import json
import requests
import util
import discord
from datetime import datetime, date, time, timezone
from discord import Color 
from discord.ext import commands
from discord import Guild, Member, Embed, Client, Intents
from discord.utils import get
from discord.ext.commands import BucketType
import os
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashCommand, SlashContext
from discord.ext.commands import Bot
from dotenv import load_dotenv
load_dotenv()
import asyncio
import auth
import logging
time = datetime.utcnow()
import urllib3
urllib3.disable_warnings()

#PREFIX
bot = commands.Bot(command_prefix="-", help_command=None)
slash = SlashCommand(bot, sync_commands=True)
#ADD VARIABLES YOU WILL BE USING THROUGHOUT MAIN.PY HERE
linebreak = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"


  




util.getActs()
f = open('acts.json', 'r')
util.actsDictionary = json.load(f)
f.close()

util.getAgents()
f = open('agents.json', 'r')
util.agentsDictionary = json.load(f)
f.close()

util.getWeapons()
f = open('weapons.json', 'r')
util.weaponsDictionary = json.load(f)
f.close()

util.getInGameWeapons()
f = open('inGameWeapons.json', 'r')
util.inGameWeaponsDictionary = json.load(f)
f.close()

f = open('logins.json', 'r') 
util.loginsDictionary = json.load(f)
f.close()

f = open('proxies.json', 'r')
util.proxies = json.load(f)
f.close()

#ON_READY
@bot.event
async def on_ready():
    print(linebreak)
    print("Cap'n is now online!")
    print(f"Logged on as {bot.user}")
    print(linebreak)                                                     
    await asyncio.sleep(1)
    print(linebreak)  



    
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}') #loads the extension in the "cogs" folder
    await ctx.send(f'Loaded "{extension}"')
    print(f'Loaded "{extension}"')

    return


@slash.slash(name="login",
              description="Link your valorant account to the bot for certain commands",
              options=[
                create_option(name='username',
                  description='Enter your riot user name (the one you use to log in to valorant)',
                  required=True,
                  option_type=3
                ),
                create_option(name='password',
                  description='Enter your riot password (the one you use to log in to valorant)',
                  required=True,
                  option_type=3
                ),
                (
                create_option(name = 'region',
                  description = 'Select your account region',
                  required = True,
                  option_type=3,
                  choices=[
                    create_choice(name='North America',
                      value='na'
                    ),
                    create_choice(name='Europe',
                      value='eu'
                    ),
                    create_choice(name='Korea',
                      value='kr'
                    ),
                    create_choice(name='Asia Pacific',
                      value='ap'
                    ),
                  ])
                )
                
              ]
            )
async def _login(ctx: SlashContext, username, password, region):
    username = util.encrypt(username)
    password = util.encrypt(password)
    discordUser = util.encrypt(str(ctx.author.id))
    f = open("logins.json", "r")
    util.loginsDictionary = json.load(f)
    f.close()
    util.loginsDictionary[discordUser] = [username, password, region]
    f = open("logins.json", "w")
    json.dump(util.loginsDictionary, f)
    f.close()
    if username == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
      username == "*"
    embedVar =   discord.Embed(title="Success!",description="CAP'N has linked your discord account to your valorant account!\n You can logout whenever with '-logout'..", color=0x00ff00)
    embedVar.add_field(name="Discord", value=f"@{ctx.author}", inline=True)
    await ctx.reply(embed=embedVar, hidden=True)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds to avoid rate limits.')
      
@slash.slash(name="checklogins",
              description="Link your valorant account to the bot for certain commands",
            )
async def _checklogins(ctx):
  hasLogin = False
  userId = str(ctx.author.id)
  userId = util.encrypt(userId)
  f = open("logins.json", "r")
  util.loginsDictionary = json.load(f)
  f.close()
  if userId in util.loginsDictionary:
    embedVar =   discord.Embed(title="Success!",description="CAP'N has found your logins in the database.", color=0x00ff00)
    await ctx.reply(embed=embedVar, hidden=True)
  else:
    embedVar =   discord.Embed(title="Error!",description="CAP'N couldn't find log ins, use /login to log in!", color=0x00ff00)
    await ctx.reply(embed=embedVar, hidden=True)
    



@slash.slash(name="store",
              description="Link your valorant account to the bot for certain commands",
            )

async def _store(ctx):
  hasLogin = False
  password = ""
  username = ""
  token = ""
  entitlement = ""
  puuid = ""
  userId = str(ctx.author.id)
  userId = util.encrypt(userId)
  f = open("logins.json", "r")
  util.loginsDictionary = json.load(f)
  f.close()
  if userId in util.loginsDictionary:
    hasLogin = True
    username = util.decrypt(util.loginsDictionary[userId][0])
    password = util.decrypt(util.loginsDictionary[userId][1])
    region = util.loginsDictionary[userId][2]
    TnEN = await auth.getToken(username, password)
    token = TnEN[0]
    entitlement = TnEN[1]
    puuid = await util.getPUUID(token)
    result = util.getStore(region, puuid, token, entitlement)
    embedvar = discord.Embed(title=f"{ctx.author.display_name}'s Store ",description="Please wait while I retreive your store!")
    embedvar.timestamp = datetime.utcnow() 
    embedvar.set_footer(text='\u200b',icon_url="https://cdn.publish0x.com/prod/fs/images/6ac0ff5feb2e723eaa18dace82b96ab9aca5ed93038ad2d739f3d58132cc3bed.png")
    await ctx.reply(embed=embedvar)
    if result == "-1":
      await ctx.send("Couldnt fetch store, try again later or log out and log back in!")
    else:
      embed= discord.Embed(title=result['displayNames'][0], color=(0xF85252))
      embed.set_thumbnail(url= f"https://media.valorant-api.com/weaponskinlevels/{result['uuids'][0]}/displayicon.png")
      embed.set_footer(text=f"")
      await ctx.channel.send(embed=embed)
      
      embed= discord.Embed(title=result['displayNames'][1], color=(0xF85252))
      embed.set_thumbnail(url= f"https://media.valorant-api.com/weaponskinlevels/{result['uuids'][1]}/displayicon.png")
      embed.set_footer(text=f"")
      await ctx.channel.send(embed=embed)
      
      embed= discord.Embed(title=result['displayNames'][2], color=(0xF85252))
      embed.set_thumbnail(url= f"https://media.valorant-api.com/weaponskinlevels/{result['uuids'][2]}/displayicon.png")
      embed.set_footer(text=f"")
      await ctx.channel.send(embed=embed)
      
      embed= discord.Embed(title=result['displayNames'][3], color=(0xF85252))
      embed.set_thumbnail(url= f"https://media.valorant-api.com/weaponskinlevels/{result['uuids'][3]}/displayicon.png")
      embed.set_footer(text=f"")
      await ctx.channel.send(embed=embed)
  if hasLogin == False:
    embedVar =   discord.Embed(title="Error!",description="CAP'N couldn't find log ins, use /login to log in!", color=0xF85252)
    await ctx.reply(embed=embedVar, hidden=True)
  
@slash.slash(name="balance",
              description="Link your valorant account to the bot for certain commands",
            )

async def _balance(ctx):
  hasLogin = False
  password = ""
  username = ""
  token = ""
  entitlement = ""
  puuid = ""
  userId = str(ctx.author.id)
  userId = util.encrypt(userId)
  f = open("logins.json", "r")
  util.loginsDictionary = json.load(f)
  f.close()
  if userId in util.loginsDictionary:
    embedvar = discord.Embed(title=f"{ctx.author.display_name}'s Balance ",description="Please wait while I retreive your balane!")
    embedvar.timestamp = datetime.utcnow() 
    embedvar.set_footer(text='\u200b',icon_url="https://cdn.publish0x.com/prod/fs/images/6ac0ff5feb2e723eaa18dace82b96ab9aca5ed93038ad2d739f3d58132cc3bed.png")
    await ctx.reply(embed=embedvar)
    hasLogin = True
    username = util.decrypt(util.loginsDictionary[userId][0])
    password = util.decrypt(util.loginsDictionary[userId][1])
    region = util.loginsDictionary[userId][2]
    TnEN = await auth.getToken(username, password)
    token = TnEN[0]
    entitlement = TnEN[1]
    puuid = await util.getPUUID(token)
    result = util.getBalance(region, puuid, token, entitlement)
    if result == "-1":
      embedVar = discord.Embed(title="Error!",description="CAP'N couldn't fetch balance, try again later or log out and log back in!", color=0xF85252)
      await ctx.reply(embed=embedVar, hidden=True)
    else:
      embed= discord.Embed(title="Valorant Points", color=(0xF85252))
      embed.set_thumbnail(url= "https://cdn.discordapp.com/attachments/887135838092296316/934184475628294145/128.png")
      embed.add_field(name="Amount", value=f"{result[0]}")
      embed.set_footer(text=f"")
      await ctx.channel.send(embed=embed)
      embed= discord.Embed(title="Radianite Points", color=(0xF85252))
      embed.set_thumbnail(url= "https://cdn.discordapp.com/attachments/887135838092296316/934184784970793060/128.png")
      embed.add_field(name="Amount", value=f"{result[1]}")
      embed.set_footer(text=f"")
      await ctx.channel.send(embed=embed)
  if hasLogin == False:
    embedVar =   discord.Embed(title="Error!",description="CAP'N couldn't find log ins, use /login to log in!", color=0xF85252)
    await ctx.reply(embed=embedVar, hidden=True)
    
    
@slash.slash(name="stats",
              description="Link your valorant account to the bot for certain commands",
            )

async def _stats(ctx):
  hasLogin = False
  password = ""
  username = ""
  token = ""
  entitlement = ""
  puuid = ""
  userId = str(ctx.author.id)
  userId = util.encrypt(userId)
  f = open("logins.json", "r")
  util.loginsDictionary = json.load(f)
  f.close()
  if userId in util.loginsDictionary:
    embedvar = discord.Embed(title=f"{ctx.author.display_name}'s stats",description="stats")
    embedvar.timestamp = datetime.utcnow() 
    embedvar.set_footer(text='\u200b',icon_url="https://cdn.publish0x.com/prod/fs/images/6ac0ff5feb2e723eaa18dace82b96ab9aca5ed93038ad2d739f3d58132cc3bed.png")
    await ctx.reply(embed=embedvar)
    hasLogin = True
    username = util.decrypt(util.loginsDictionary[userId][0])
    password = util.decrypt(util.loginsDictionary[userId][1])
    region = util.loginsDictionary[userId][2]
    TnEN = await auth.getToken(username, password)
    token = TnEN[0]
    entitlement = TnEN[1]
    puuid = await util.getPUUID(token)
    result = util.stats(region, puuid, token, entitlement)
    
      
    print(result)

@slash.slash(name="matchstats",
              description="Link your valorant account to the bot for certain commands",
            )
@commands.cooldown(1, 60, commands.BucketType.default)
async def matchstats(ctx):
  hasLogin = False
  password = ""
  username = ""
  token = ""
  entitlement = ""
  puuid = ""
  userId = str(ctx.author.id)
  userId = util.encrypt(userId)
  f = open("logins.json", "r")
  util.loginsDictionary = json.load(f)
  f.close()
  if userId in util.loginsDictionary:
    embedvar = discord.Embed(title=f"Warning!",description="retreiving match stats will take 5-15 seconds, if it takes more than 20 seconds, assume we've been rate limited and try again in 2 minutes!")
    embedvar.timestamp = datetime.utcnow() 
    embedvar.set_footer(text='\u200b',icon_url="https://cdn.publish0x.com/prod/fs/images/6ac0ff5feb2e723eaa18dace82b96ab9aca5ed93038ad2d739f3d58132cc3bed.png")
    await ctx.reply(embed=embedvar)
    hasLogin = True
    username = util.decrypt(util.loginsDictionary[userId][0])
    password = util.decrypt(util.loginsDictionary[userId][1])
    region = util.loginsDictionary[userId][2]
    TnEN = await auth.getToken(username, password)
    token = TnEN[0]
    entitlement = TnEN[1]
    puuid = await util.getPUUID(token)
    result = util.matchStats(region, puuid, entitlement, token)
    if result['status'] == -1:
      embedvar = discord.Embed(title=f"Error!",description="Couldnt fetch match stats, to use this command you must be currently in a game. Agent select does not count!")
      embedvar.timestamp = datetime.utcnow()
      embedvar.set_footer(text='\u200b',icon_url="https://cdn.publish0x.com/prod/fs/images/6ac0ff5feb2e723eaa18dace82b96ab9aca5ed93038ad2d739f3d58132cc3bed.png")
      await ctx.reply(embed=embedvar, hidden=True)
    else:
      if result['ffa'] == 0:
        embed= discord.Embed(title=f"{ctx.author}'s Match Stats", color=(0xF85252))
        embed.set_thumbnail(url= "https://cdn.discordapp.com/attachments/822383742084579328/934640243657830410/85.png")
        embed.add_field(name="Blue Team:", value="Heres everyone on the blue team")
        for i in range(len(result['blueTeam'])):
          embed.add_field(name=f"{result['blueTeam'][i]['name']} ({result['blueTeam'][i]['agent']})", value=f"rank: {result['blueTeam'][i]['rank']}, rr: {result['blueTeam'][i]['rr']}, peak: {result['blueTeam'][i]['peak']}, peak EP/A: {result['blueTeam'][i]['peakSeason']}")
        await ctx.send(embed=embed)
        embed2= discord.Embed(title=f"{ctx.author}'s Match Stats", color=(0xF85252))
        embed2.set_thumbnail(url= "https://cdn.discordapp.com/attachments/822383742084579328/934640243657830410/85.png")
        embed2.add_field(name="Red Team:", value="Heres everyone on the red team")
        for i in range(len(result['redTeam'])):
          embed2.add_field(name=f"{result['redTeam'][i]['name']} ({result['redTeam'][i]['agent']})", value=f"rank: {result['redTeam'][i]['rank']}, rr: {result['redTeam'][i]['rr']}, peak: {result['redTeam'][i]['peak']}, peak EP/A: {result['redTeam'][i]['peakSeason']}", inline = True)
        await ctx.send(embed=embed2)
      else:
        embed= discord.Embed(title=f"{ctx.author}'s Match Stats", color=(0xF85252))
        embed.set_thumbnail(url= "https://cdn.discordapp.com/attachments/822383742084579328/934640243657830410/85.png")
        embed.add_field(name="Players: ", value='Heres all players in your lobby')
        for i in range(len(result['players'])):
          embed.add_field(name=f"{result['players'][i]['name']} ({result['players'][i]['agent']})", value=f"rank: {result['players'][i]['rank']}, rr: {result['players'][i]['rr']}, peak: {result['players'][i]['peak']}, peak EP/A: {result['players'][i]['peakSeason']}")
        await ctx.send(embed=embed)
  if hasLogin == False:
    await ctx.send("Couldnt find log ins, use /login to log in!")
    
@matchstats.error
async def command_name_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
          embedvar = discord.Embed(title=f"Warning!",description=f"Please wait **{error.retry_after:.2f}**s before using this command again!")
          embedvar.timestamp = datetime.utcnow() 
          embedvar.set_footer(text='\u200b',icon_url="https://cdn.publish0x.com/prod/fs/images/6ac0ff5feb2e723eaa18dace82b96ab9aca5ed93038ad2d739f3d58132cc3bed.png")
          await ctx.reply(embed=embedvar)
    

          
@bot.command()
async def logout(ctx):
  hasLogin = False
  userId = str(ctx.message.author.id)
  userId = util.encrypt(userId)
  f = open("logins.json", "r")
  util.loginsDictionary = json.load(f)
  f.close()
  if userId in util.loginsDictionary:
    util.loginsDictionary.pop(userId)
    f = open("logins.json", "w")
    json.dump(util.loginsDictionary, f)
    f.close()
    hasLogin = True
  if hasLogin:
    await ctx.send("Successfully logged out!")
  else:
    await ctx.send("Cant log out if you were never logged in!")


@bot.command()
async def rank(ctx, name=' ', region=' ', *, act=' '):
  act = act.upper()
  region = region.lower()
  if name == ' ':
    await ctx.send("Error, please specify a name! usage 'rank Spherical#balls **E4A1**' where bold means optional!")
  elif util.indexOf(name, '#') == -1:
    await ctx.send("Invalid name! usage 'rank Spherical#balls **E4A1**' where bold means optional!")
  else:
    if act == ' ':
      act = (util.getCurrentSeason())
    else:
      validAct = False
      for i in util.actsDictionary:
        if act == i:
          validAct = True
      if validAct == False:
        act = (util.getCurrentSeason())
    if region == 'na' or region == 'eu' or region == 'ap' or region ==  'kr':
      tag = name[util.indexOf(name, '#')+1:]
      name = name[0:util.indexOf(name, '#')]
      await ctx.send(f"fetching {name}#{tag}'s rank in {act}!")
      output = await util.getRankByName(name, tag, region, act)
      url = f'https://valorant-api.com/v1/competitivetiers'
      y = requests.get(url).json()
      if output[0] == 50:
        embed= discord.Embed(title="UNRANKED", color=(0x5b5b5b))
        embed.set_thumbnail(url= "https://media.valorant-api.com/competitivetiers/564d8e28-c226-3180-6285-e48a390db8b1/0/largeicon.png")
        embed.add_field(name="Uh oh..", value=f"{name} has never played ranked before!")
        embed.set_footer(text=f"{name}'s rank in {act}")
        await ctx.channel.send(embed=embed)
      elif output[0] == -1:
        await ctx.send("Couldnt fetch rank! This could mean we are rate limited. Try again in 10-30 seconds")
      elif output[0] == 100:
        embed= discord.Embed(title="UNRANKED", color=(0x5b5b5b))
        embed.set_thumbnail(url= "https://media.valorant-api.com/competitivetiers/564d8e28-c226-3180-6285-e48a390db8b1/0/largeicon.png")
        embed.add_field(name="Peak rank:", value=f"{output[4]} in {output[6]}")
        embed.set_footer(text=f"{name} did not play ranked in {act}")
        await ctx.channel.send(embed=embed)
      elif output[0] == 150:
        embed= discord.Embed(title="UNRANKED", color=(0x5b5b5b))
        embed.set_thumbnail(url= "https://media.valorant-api.com/competitivetiers/564d8e28-c226-3180-6285-e48a390db8b1/0/largeicon.png")
        embed.add_field(name="Peak rank:", value=f"{output[4]} in {output[6]}")
        embed.set_footer(text=f"{name}'s rank in {act}")
        await ctx.channel.send(embed=embed)
      elif output[0] == 200:
        embed= discord.Embed(title=f"{output[1]}", description=f"with {output[2]} rr", color=(util.rankColors[output[3]]))
        embed.set_thumbnail(url= y['data'][0]['tiers'][output[3]]['largeIcon'])
        embed.add_field(name="Peak rank:", value=f"{output[4]} in {output[6]}")
        embed.set_footer(text=f"{name}'s rank in {act}")
        await ctx.channel.send(embed=embed)
    else:
      await ctx.send("Invalid region! Supported regions are NA, EU, KR and AP")


for file in os.listdir("./cogs"): 
    if file.endswith(".py"):
        name = file[:-3] 
        bot.load_extension(f"cogs.{name}") 

token = os.environ['TOKEN']
bot.run(token)
