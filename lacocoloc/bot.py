import redis

from .speaker import speak
from .utils import debug

redis_client = redis.Redis(host='ec2-63-35-120-48.eu-west-1.compute.amazonaws.com', port='10449',
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
