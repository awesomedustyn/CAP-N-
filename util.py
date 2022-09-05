import os
import json
import asyncio
import aiohttp
import requests
import auth

from datetime import datetime
from datetime import date


weaponsDictionary = {}
inGameWeaponsDictionary = {}
agentsDictionary = {}
actsDictionary = {}
loginsDictionary = {}
proxies = []
rankColors = {0:0x5b5b5b,1:0x5b5b5b,2:0x5b5b5b,3:0x404040,4:0x404040,5:0x404040,6:0x86592d,7:0x86592d,8:0x86592d,9:0xbfbfbf,10:0xbfbfbf,11:0xbfbfbf,12:0xe6b800,13:0xe6b800,14:0xe6b800,15:0x00a3cc,16:0x00a3cc,17:0x00a3cc,18:0xff66cc,19:0xff66cc,20:0xff66cc,21:0xff1a1a,22:0xff1a1a,23:0xff1a1a,24:0xffffff}
defaultRegion = 'na'
clientPlatform = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"

async def getPUUID(token):
  session = aiohttp.ClientSession()
  url = 'https://auth.riotgames.com/userinfo'
  headers = {
      'Authorization': f'Bearer {token}'
  }
  async with session.get(url, json = {}, headers=headers) as req3:
    data = await req3.json()
  puuid = data["sub"]
  await session.close()
  return puuid

def getActs():
    url = 'https://valorant-api.com/v1/seasons'
    r = requests.get(url)
    y = r.json()
    episode = 0
    f = open("acts.json", "r")
    actsDictionary = json.load(f)
    f.close()
    for i in range(len(y['data'])):
      if (i-1)%4 == 0:
        episode += 1
      elif i == 0:
        continue
      elif (i-1)%4 == 1:
        actsDictionary['E'+str(episode)+'A1'] = y['data'][i]['uuid']
      elif (i-1)%4 == 2:
        actsDictionary['E'+str(episode)+'A2']= y['data'][i]['uuid']
      elif (i-1)%4 == 3:
        actsDictionary['E'+str(episode)+'A3'] = y['data'][i]['uuid']
    f = open("acts.json", "w")
    json.dump(actsDictionary, f)
    f.close()

def getAgents():
    url = 'https://valorant-api.com/v1/agents'
    r = requests.get(url)
    y = r.json()
    f = open("agents.json", "r")
    agentsDictionary = json.load(f)
    f.close()
    for i in range(len(y['data'])):
      agentsDictionary[y['data'][i]['uuid']] = y['data'][i]['displayName']
      agentsDictionary[y['data'][i]['uuid'].upper()] = y['data'][i]['displayName']
    f = open("agents.json", "w")
    json.dump(agentsDictionary, f)
    f.close()

def getWeapons():
    url = 'https://valorant-api.com/v1/weapons'
    r = requests.get(url)
    y = r.json()
    f = open("weapons.json", "r")
    weaponsDictionary = json.load(f)
    for i in range(len(y['data'])):
      weaponsDictionary[y['data'][i]['uuid']] = y['data'][i]['displayName']
      for n in range(len(y['data'][i]['skins'])):
        weaponsDictionary[y['data'][i]['skins'][n]['uuid']] = y['data'][i]['skins'][n]['displayName']
        for j in range(len(y['data'][i]['skins'][n]['chromas'])):
          weaponsDictionary[y['data'][i]['skins'][n]['chromas'][j]['uuid']] = y['data'][i]['skins'][n]['displayName']
        for l in range(len(y['data'][i]['skins'][n]['levels'])):
          weaponsDictionary[y['data'][i]['skins'][n]['levels'][l]['uuid']] = y['data'][i]['skins'][n]['displayName']
    f = open("weapons.json", "w")
    json.dump(weaponsDictionary, f)
    f.close()

def getInGameWeapons():
    url = 'https://valorant-api.com/v1/weapons'
    r = requests.get(url)
    y = r.json()
    f = open("inGameWeapons.json", "r")
    inGameWeaponsDictionary = json.load(f)
    for i in range(len(y['data'])):
      inGameWeaponsDictionary[y['data'][i]['uuid']] = y['data'][i]['displayName']
    f = open("inGameWeapons.json", "w")
    json.dump(inGameWeaponsDictionary, f)
    f.close()

def shiftProxies():
  proxyShift = proxies[0]
  proxies.pop(0)
  proxies.append(proxyShift)
    

def indexOf(s, find):
    for i in range(len(s)):
        if s[i:i+len(find)] == find:
            return i
    return -1

def encrypt(s):
  newS = ""
  chars = """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*();:'-~"[{]}.>,<|1234567890"""
  chars2 = """0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*();:'-~"[{]}.>,<|123456789"""
  charList = []
  charList2 = []
  ASCIIchars = []
  for i in chars:
    charList.append(i)
  for i in chars2:
    charList2.append(i)
  for i in s:
    newS += chars2[chars.index(i)]
  for i in newS:
    ASCIIchars.append(ord(i))
  for i in range(len(ASCIIchars)):
    ASCIIchars[i] += 5
    ASCIIchars[i] = str(ASCIIchars[i])
  newS = ""
  for i in ASCIIchars:
    newS += i+'.'
  return newS

def decrypt(s):
  newS = ""
  chars = """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*();:'-~"[{]}.>,<|1234567890"""
  chars2 = """0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*();:'-~"[{]}.>,<|123456789"""
  ASCIIchars = []
  while s != '':
    ASCIIchars.append(s[0:indexOf(s,'.')])
    s = s[indexOf(s,'.')+1:]
  for i in range(len(ASCIIchars)):
    ASCIIchars[i] = int(ASCIIchars[i]) - 5
  for i in ASCIIchars:
    newS += str(chr(i))
  s = ""
  for i in newS:
    s += chars[chars2.index(i)]
  return s

def getValoVersion():
  url = 'https://valorant-api.com/v1/version'
  r = requests.get(url)
  y = r.json()
  return y['data']['riotClientVersion']

def getCurrentSeason():
  url = 'https://valorant-api.com/v1/seasons'
  r = requests.get(url)
  y = r.json()
  episode = 0
  count = 0
  currentDate = datetime.today().strftime('%Y-%m-%d')
  for i in y['data']:
    if (count - 1) % 4 == 0:
      episode += 1
    else:
      seStart = i['startTime'][0:indexOf(i['startTime'], 'T')]
      seEnd = i['endTime'][0:indexOf(i['endTime'], 'T')]
      cDate = date(int(currentDate[0:4]), int(currentDate[5:7]), int(currentDate[8:10]))
      sDate = date(int(seStart[0:4]), int(seStart[5:7]), int(seStart[8:10]))
      eDate = date(int(seEnd[0:4]), int(seEnd[5:7]), int(seEnd[8:10]))
      if (cDate-sDate).days >= 0 and (cDate-eDate).days < 0:
        if (count - 1) % 4 == 1:
          return f'E{episode}A1'
        if (count - 1) % 4 == 2:
          return f'E{episode}A2'
        if (count - 1) % 4 == 3:
          return f'E{episode}A3'
    count += 1

def getMaxRank(region, en, t, puuid):
  url = f'https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}'
  headers = {
        'X-Riot-Entitlements-JWT': en,
        'Authorization': f'Bearer {t}',
        'X-Riot-ClientVersion': getValoVersion(),
        'X-Riot-ClientPlatform': clientPlatform
  }
  r = requests.get(url, json = {}, headers=headers)
  y = r.json()
  if str(r.status_code) != "200":
    return -1
  maxRank = [-1,'']
  seasons = y["QueueSkills"]["competitive"].get("SeasonalInfoBySeasonID")
  if seasons is not None:
    for season in y["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"]:
      if y["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][season]["WinsByTier"] is not None:
        for winByTier in y["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][season]["WinsByTier"]:
          if int(winByTier) > maxRank[0]:
            maxRank[1] = list(actsDictionary.keys())[list(actsDictionary.values()).index(season)]
            maxRank[0] = int(winByTier)
  return maxRank
               

def getOtherPUUID(name, tagline, region):
    url = f'https://api.henrikdev.xyz/valorant/v2/mmr/na/{name}/{tagline}'
    r = requests.get(url)
    y = r.json()
    if r.status_code == 200:
        puuid = y['data']['puuid']
        return puuid
    elif r.status_code == 429:
        return "429"
    elif r.status_code == 500:
      return "500"
    else:
      return "-1"

async def getRankByName(name, tag, region, act):
  user = os.environ['user']
  password = os.environ['password']
  TnEN = await auth.getToken(user, password)
  t = TnEN[0]
  en = TnEN[1]
  puuid = getOtherPUUID(name, tag, region)
  if puuid == "429":
    return "We've been rate limited! Try again in 10 seconds"
  elif puuid == "500":
    return f"Couldnt find player {name}#{tag}"
  url = f'https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}'
  headers = {
    'X-Riot-Entitlements-JWT':en,
    'Authorization': f'Bearer {t}',
    'X-Riot-ClientVersion': getValoVersion(),
    'X-Riot-ClientPlatform': clientPlatform
  }
  r = requests.get(url, headers=headers)
  y = r.json()
  status = str(r.status_code)
  r = requests.get('https://valorant-api.com/v1/competitivetiers')
  x = r.json()
  maxRank = getMaxRank(region, en, t, puuid)
  if maxRank[0] == -1:
    output = f"{name}#{tag} from {region} is UNRANKED. They have not played ranked."
    output = [50, "UNRANKED", "-1", -1, -1, -1, -1]
    return output
  else:
    maxrank = x['data'][0]['tiers'][maxRank[0]]['tierName']
    maxSeason = maxRank[1]
    if status != "200":
      output = [-1, -1, -1, -1, -1, -1, -1]
      return output
    else:
      try:
        rankTIER = y["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][actsDictionary[act]]["CompetitiveTier"]
        rank = x['data'][0]['tiers'][rankTIER]['tierName']
        if rank == 'UNRANKED':
          output = [150, "UNRANKED", "-1", rankTIER, maxrank, maxRank, maxSeason]
          return output
        else:
          mmr = y["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][actsDictionary[act]]["RankedRating"]
          mmr = str(mmr)
          if rankTIER < 21:
            if len(mmr) > 2:
              mmr = mmr[1:]
            if len(mmr) > 3:
              mmr = mmr[2:]
          output = f"{name}#{tag} from {region}'s rank in {act} is {rank} with {mmr} rr. Their peak rank was {maxrank} in {maxSeason}"
          output = [200, rank, mmr, rankTIER, maxrank, maxRank, maxSeason]
          return output
      except KeyError:
        output = [100, -1, -1, -1, maxrank, maxRank, maxSeason]
        return output

def getMatchRanks(region, en, t, puuid):
  act = getCurrentSeason()
  url = f'https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}'
  headers = {
        'X-Riot-Entitlements-JWT': en,
        'Authorization': f'Bearer {t}',
        'X-Riot-ClientVersion': getValoVersion(),
        'X-Riot-ClientPlatform': clientPlatform
  }
  r = requests.get(url, headers=headers)
  y = r.json()
  status = str(r.status_code)
  r = requests.get('https://valorant-api.com/v1/competitivetiers')
  x = r.json()
  maxRank = getMaxRank(region, en, t, puuid)
  if maxRank[0] == -1:
    rank = ["UNRANKED", "No RR",  "UNRANKED", "Never played ranked"]
    return rank
  maxrank = x['data'][0]['tiers'][maxRank[0]]['tierName']
  maxSeason = maxRank[1]
  if status != "200":
    return "-1"
  try:
    rankTIER = y["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][actsDictionary[act]]["CompetitiveTier"]
    rank = x['data'][0]['tiers'][rankTIER]['tierName']
    if rank == 'UNRANKED':
      output = ['UNRANKED', 'No RR', maxrank, maxSeason]
      return output
    else:
      mmr = y["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][actsDictionary[act]]["RankedRating"]
      mmr = str(mmr)
      if rankTIER < 21:
        if len(mmr) > 2:
          mmr = mmr[1:]
        if len(mmr) > 3:
          mmr = mmr[2:]
      output = [rank, mmr, maxrank, maxSeason]
      return output
  except KeyError:
    output = ['UNRANKED', 'No RR', maxrank, maxSeason]
    return output

def getBalance(region, puuid, t, en):
  url = f'https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}'
  headers = headers = {
      'X-Riot-Entitlements-JWT': en,
      'Authorization': f'Bearer {t}'
  }
  r = requests.get(url, headers=headers)
  balance = [0,0]
  if str(r.status_code) == "200":
    y = r.json()
    balance[0] = y['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
    balance[1] = y['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7']
    return balance
  else:
    return [-1, -1]


def getStore(region, puuid, t, en):
  url = f'https://pd.{region}.a.pvp.net/store/v2/storefront/{puuid}'
  headers = headers = {
        'X-Riot-Entitlements-JWT': en,
        'Authorization': f'Bearer {t}'
  }
  r = requests.get(url, headers=headers)
  singleItems = ['', '', '', '']
  y = r.json()
  if str(r.status_code) == "200":
    singleItems[0] = weaponsDictionary[y['SkinsPanelLayout']['SingleItemOffers'][0]]
    singleItems[1] = weaponsDictionary[y['SkinsPanelLayout']['SingleItemOffers'][1]]
    singleItems[2] = weaponsDictionary[y['SkinsPanelLayout']['SingleItemOffers'][2]]
    singleItems[3] = weaponsDictionary[y['SkinsPanelLayout']['SingleItemOffers'][3]]
    output = {'uuids': [y['SkinsPanelLayout']['SingleItemOffers'][0],y['SkinsPanelLayout']['SingleItemOffers'][1],y['SkinsPanelLayout']['SingleItemOffers'][2],y['SkinsPanelLayout']['SingleItemOffers'][3]], 'displayNames': [singleItems[0],singleItems[1],singleItems[2],singleItems[3]]}
    return output
  else:
    return "-1"

def getNameFromPUUID(puuid, region, token):
  output = ['','']
  url = f"https://pd.{region}.a.pvp.net/name-service/v2/players"
  headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
  }
  response = requests.put(url, headers=headers, json=[puuid], verify=False)
  output[0] = response.json()[0]["GameName"]
  output[1] = response.json()[0]["TagLine"]
  return output


def getCurrentMatchID(region, puuid, entitlement, token):
  url = f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/players/{puuid}'
  headers = {
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
  }
  r = requests.get(url, headers=headers)
  y = r.text
  print(y)
  if str(r.status_code) != "200":
    return "-1"
  else:
    output = y[indexOf(y,'MatchID')+10:indexOf(y,'","Version')]
    return output

def matchStats(region, puuid, entitlement, token):
  matchID = getCurrentMatchID(region, puuid, entitlement, token)
  if matchID != "-1":
    matchid = matchID
  else:
    output = {'status': -1}
    return output
  url = f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/matches/{matchid}'
  url2 = f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/matches/{matchid}/loadouts'
  headers = {
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
  }
  r = requests.get(url, headers=headers)
  y = r.json()
  r2 = requests.get(url2, headers=headers)
  x = r2.json()
  loadout = x['Loadout']['Items']
  print(y)
  print(x)
  if str(r.status_code) != "200":
    output = {'status': -1}
    return output
  players = y['Players']
  ffa = False
  if y['ModeID'] == '/Game/GameModes/Deathmatch/DeathmatchGameMode.DeathmatchGameMode_C':
    ffa = True
  if ffa == False:
    for i in loadout:
      skin = weaponsDictionary[loadout[i]['9c82e19d-4575-0200-1a81-3eacf00cf872']['Sockets']['3ad1b2b2-acdb-4524-852f-954a76ddae0a']["Item"]["ID"]]
      print(skin)
    output = {}
    output['status'] = 200
    output['ffa'] = 0
    output['blueTeam'] = []
    output['redTeam'] = []
    for i in range(len(players)):
      if y['Players'][i]['TeamID'] == "Blue":
        rankData = getMatchRanks(region, entitlement, token, y['Players'][i]['Subject'])
        nameFromPUUID = getNameFromPUUID(y['Players'][i]['Subject'], region, token)
        name = nameFromPUUID[0] + "#" + nameFromPUUID[1]
        output['blueTeam'].append({'puuid': y['Players'][i]['Subject'], 'name': name, 'agent': agentsDictionary[y['Players'][i]['CharacterID']], 'rank': rankData[0], 'rr': rankData[1], 'peak': rankData[2], 'peakSeason': rankData[3]})
      else:
        rankData = getMatchRanks(region, entitlement, token, y['Players'][i]['Subject'])
        nameFromPUUID = getNameFromPUUID(y['Players'][i]['Subject'], region, token)
        name = nameFromPUUID[0] + "#" + nameFromPUUID[1]
        output['redTeam'].append({'puuid': y['Players'][i]['Subject'], 'name': name, 'agent': agentsDictionary[y['Players'][i]['CharacterID']], 'rank': rankData[0], 'rr': rankData[1], 'peak': rankData[2], 'peakSeason': rankData[3]})
    return output
  else:
    output = {}
    output['status'] = 200
    output['ffa'] = 1
    output['players'] = []
    for i in range(len(players)):
      rankData = getMatchRanks(region, entitlement, token, y['Players'][i]['Subject'])
      nameFromPUUID = getNameFromPUUID(y['Players'][i]['Subject'], region, token)
      name = nameFromPUUID[0] + "#" + nameFromPUUID[1]
      output['players'].append({'puuid': y['Players'][i]['Subject'], 'name': name, 'agent': agentsDictionary[y['Players'][i]['CharacterID']], 'rank': rankData[0], 'rr': rankData[1], 'peak': rankData[2], 'peakSeason': rankData[3]})
    return output
