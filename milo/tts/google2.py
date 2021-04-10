import os
import uuid

import subprocess

import io
from google.cloud import texttospeech
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

from milo.tts.__interface__ import TTSInterface


class GoogleTTS2(TTSInterface):

    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()

        # Build the voice request
        # noinspection PyTypeChecker
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="fr-FR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        # Select the type of audio file you want returned
        # noinspection PyTypeChecker
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def synthesize_speech(self, text: str) -> None:
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )

        play(AudioSegment.from_file(io.BytesIO(response.audio_content), format="mp3"))

