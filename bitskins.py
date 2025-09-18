import pyotp
from logger import logger


import requests
import json

auth_key = '4a0d2e94379013db209e42d19fe48f5ac2c319cf450af00d16eaa12f018c5d2e'
data = {
  "limit": 30,
  "offset": 0,

  }


headers = {'x-apikey': auth_key}
#res = requests.post('https://api.bitskins.com/market/search/730', headers=headers, json=data)
#response = json.loads(res.text)
#print(response)


# get a token that's valid right now
my_secret = 'MMZWMYLGGIZWMYTCMVRTSMLGGUYGEZLG'
#671355
#my_token = pyotp.TOTP(my_secret)

# print the valid token
#print(my_token.now())

def generate_2fa_code(secret):
    """Генерирует текущий 2FA код для BitSkins с использованием секрета."""
    try:
        totp = pyotp.TOTP(secret)
        return totp.now()
    except Exception as e:
        logger.error(f"Ошибка генерации 2FA кода: {e}")
        return None