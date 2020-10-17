import redis

from .speaker import speak
from .utils import debug

REDIS_URL = 'redis://h:p536dfe7c3cbbcc9c049d0f0d127697e6fb9c63e17b15b7ab2ad50b22d30088fb@ec2-54-170-172-162.eu-west-1.compute.amazonaws.com:12319'

redis_client = redis.Redis(host='ec2-54-170-172-162.eu-west-1.compute.amazonaws.com', port='12319',
                           password='p536dfe7c3cbbcc9c049d0f0d127697e6fb9c63e17b15b7ab2ad50b22d30088fb')


def bot():
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
