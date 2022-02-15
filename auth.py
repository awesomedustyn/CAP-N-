import asyncio
import aiohttp
import re

async def getToken(user, password):
  session = aiohttp.ClientSession()
  url = "https://auth.riotgames.com/api/v1/authorization"
  headers = {
        "User-Agent": 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)'
        }
  body = {
        "client_id": "play-valorant-web-prod",
        "nonce": "1",
        "redirect_uri": "https://playvalorant.com/opt_in",
        "response_type": "token id_token"
    }

  await session.post(url, json=body, headers=headers)

  body = {
        "type": "auth",
        "username": user,
        "password": password
    }
  async with session.put('https://auth.riotgames.com/api/v1/authorization', json=body, headers=headers) as r2:
    data = await r2.json()
  
  if data['type'] == 'auth':
    print("2")
    await session.close()
    return ["-1", "0"]
  elif data['type'] == 'multifactor':
    print("3")
    await session.close()
    return ["-2", "0"]

  pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
  data = pattern.findall(data['response']['parameters']['uri'])[0]
  token = data[0]

  headers = {
        'Authorization': f'Bearer {token}',
    }
  async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r3:
    data = await r3.json()
  en = data['entitlements_token']

  await session.close()
  return [token, en]
