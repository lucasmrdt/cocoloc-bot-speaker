from google.cloud import texttospeech
import playsound
import os

from .utils import debug

TMP_FILE = '/tmp/output.mp3'
CURRENT_FOLDER = os.path.dirname(__file__)
NOTIFICATION_EFFECT_FILE = os.path.join(
    CURRENT_FOLDER, '../assets/notification.mp3')

client = texttospeech.TextToSpeechClient()
FEMALE_VOICE = texttospeech.VoiceSelectionParams(
    language_code="fr-FR-Standard-A", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
MALE_VOICE = texttospeech.VoiceSelectionParams(
    language_code="fr-FR-Standard-A", ssml_gender=texttospeech.SsmlVoiceGender.MALE
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=.85
)


def create_voice(msg: str, female_voice=False):
    voice = FEMALE_VOICE if female_voice else MALE_VOICE
    synthesis_input = texttospeech.SynthesisInput(ssml=msg)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(TMP_FILE, 'wb') as out:
        out.write(response.audio_content)


def speak(msg, female_voice=False):
    try:
        debug('saying', msg)
        create_voice(f'<speak>{msg}</speak>', female_voice=female_voice)
        playsound.playsound(NOTIFICATION_EFFECT_FILE)
        playsound.playsound(TMP_FILE)
    except Exception as e:
        debug('error', f'fail to speak with {e}')
