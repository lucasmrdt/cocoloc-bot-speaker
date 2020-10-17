from google.cloud import texttospeech
import playsound

from .utils import debug

TMP_FILE = '/tmp/output.mp3'

client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code="fr-FR-Standard-A", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)


def create_voice(msg: str):
    synthesis_input = texttospeech.SynthesisInput(ssml=msg)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(TMP_FILE, 'wb') as out:
        out.write(response.audio_content)


def speak(msg):
    try:
        debug('saying', msg)
        create_voice(f'<speak><break time="1s"/>{msg}</speak>')
        playsound.playsound(TMP_FILE)
    except Exception as e:
        debug('error', f'fail to speak with {e}')
