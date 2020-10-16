import time
import platform
import redis
import playsound
import requests

REDIS_URL = 'redis://h:p536dfe7c3cbbcc9c049d0f0d127697e6fb9c63e17b15b7ab2ad50b22d30088fb@ec2-54-170-172-162.eu-west-1.compute.amazonaws.com:12319'

redis_server = redis.Redis(host='ec2-54-170-172-162.eu-west-1.compute.amazonaws.com', port='12319',
                           password='p536dfe7c3cbbcc9c049d0f0d127697e6fb9c63e17b15b7ab2ad50b22d30088fb')

def create_audio(msg):
    res = requests.post('https://ttsmp3.com/makemp3_new.php', data={'msg': msg, 'lang': 'Celine', 'source': 'ttsmp3'})
    data = res.json()
    if data['Error']:
        raise Exception('error while creating audio file')
    return data['URL']

def speak(msg):
    try:
        url = create_audio(msg)
        playsound.playsound(url)
    except Exception as e:
        print(f'error: fail to speak - {e}')

def bot():
    print('waiting messages ...')
    while True:
        response = redis_server.lpop('msg')
        if response:
            msg = response.decode('utf-8')
            print(f'saying: "{msg}"')
            speak(msg)
        time.sleep(1)


if __name__ == '__main__':
    try:
        bot()
    except KeyboardInterrupt:
        print('bye !')
