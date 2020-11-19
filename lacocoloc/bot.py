import redis
import time
import requests
import re

from .speaker import speak
from .utils import debug

REDIS_URL_REGEX = r'.+://.+:(.+)@(.+):(.+)'


def get_redis_client():
    response = requests.get('https://la-cocoloc.herokuapp.com/redis-url')
    redis_url = response.json()['url']
    matches = re.match(REDIS_URL_REGEX, redis_url)
    password, host, port = matches.group(1), matches.group(2), matches.group(3)
    redis_client = redis.Redis(host=host, port=port, password=password)
    return redis_client

def bot():
    redis_client = get_redis_client()
    debug('waiting message...')
    while True:
        _, response = redis_client.brpop('tts', timeout=0)
        if response:
            msg = response.decode('utf-8')
            speak(msg)


def main():
    while True:
        try:
            bot()
        except KeyboardInterrupt:
            debug('quit')
            break
        except Exception as e:
            debug('error', e)
            time.sleep(10)

