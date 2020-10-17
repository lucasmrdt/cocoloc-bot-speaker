from google.cloud import texttospeech
import time
import platform
import redis
import playsound
import datetime

REDIS_URL = 'redis://h:p536dfe7c3cbbcc9c049d0f0d127697e6fb9c63e17b15b7ab2ad50b22d30088fb@ec2-54-170-172-162.eu-west-1.compute.amazonaws.com:12319'

redis_server = redis.Redis(host='ec2-54-170-172-162.eu-west-1.compute.amazonaws.com', port='12319',
                           password='p536dfe7c3cbbcc9c049d0f0d127697e6fb9c63e17b15b7ab2ad50b22d30088fb')
client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code="fr-FR-Standard-A", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

def debug(action, description=None):
    now = datetime.datetime.now()
    if description:
        print(f'[{now.strftime("%d/%m %H:%M")}] {action}: "{description}"')
    else:
        print(f'[{now.strftime("%d/%m %H:%M")}] {action}')

def create_voice(msg):
    synthesis_input = texttospeech.SynthesisInput(ssml=msg)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open("voice.mp3", "wb") as out:
        out.write(response.audio_content)

def speak(msg):
    try:
        create_voice(msg)
        playsound.playsound('./voice.mp3')
    except Exception as e:
        debug('error', f'fail to speak with {e}')

def bot():
    debug('waiting message...')
    while True:
        _, response = redis_server.brpop('msg', timeout=0)
        if response:
            msg = response.decode('utf-8')
            debug('saying', msg)
            speak(f'<speak><break time="1s"/>{msg.capitalize()}</speak>')


if __name__ == '__main__':
    while True:
        try:
            bot()
        except KeyboardInterrupt:
            debug('quit')
            break
        except Exception as e:
            debug('error', e)
