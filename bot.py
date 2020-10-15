import pyttsx3
import time
import platform
import redis

REDIS_URL = 'redis://h:p536dfe7c3cbbcc9c049d0f0d127697e6fb9c63e17b15b7ab2ad50b22d30088fb@ec2-54-170-172-162.eu-west-1.compute.amazonaws.com:12319'
VOICE_BY_SYSTEM = {
    'Darwin': 'com.apple.speech.synthesis.voice.amelie'
}


redis_server = redis.Redis(host='ec2-54-170-172-162.eu-west-1.compute.amazonaws.com', port='12319',
                           password='p536dfe7c3cbbcc9c049d0f0d127697e6fb9c63e17b15b7ab2ad50b22d30088fb')

engine = pyttsx3.init()
try:
    system = platform.system()
    assert system in VOICE_BY_SYSTEM
    engine.setProperty('voice', VOICE_BY_SYSTEM[system])
except AssertionError:
    print('warning: no voice configured for your system')


def bot():
    print('waiting messages ...')
    while True:
        response = redis_server.lpop('msg')
        if response:
            msg = response.decode('utf-8')
            print(f'saying: "{msg}"')
            engine.say(msg)
            engine.runAndWait()
        time.sleep(1)


if __name__ == '__main__':
    bot()
