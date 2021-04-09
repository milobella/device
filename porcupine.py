#!/usr/bin/env python3
import json

import os
import subprocess

import requests
import speech_recognition as sr
import struct
import pyaudio
import pvporcupine
from gtts import gTTS
from playsound import playsound
import uuid

r = sr.Recognizer()
m = sr.Microphone()

porcupine = None
sound = None
audio_stream = None


def talk(text):
    tts = gTTS(text=text, lang='fr', lang_check=False)
    name = uuid.uuid4()
    tts.save(f"{name}.mp3")

    from platform import system
    system = system()

    if system == 'Windows':
        playsound(f"{name}.mp3")
    else:
        subprocess.Popen(["mpg321", f"{name}.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.remove(f"{name}.mp3")


try:
    talk("Je suis prête")
    porcupine = pvporcupine.create(keywords=["picovoice"])

    sound = pyaudio.PyAudio()

    audio_stream = sound.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)

    with m as source:
        r.adjust_for_ambient_noise(source)

    listening = False

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            listening = True
            print("Hotword Detected")

        if listening:
            with m as source:
                audio = r.listen(source)
            try:
                value = r.recognize_google(audio, language="fr-FR")
                print("You said {}".format(value))
                milobella_response = requests.post(
                    'https://milobella.com:10443/talk/text',
                    data=json.dumps({'text': value}),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + os.environ['MILOBELLA_AUTHORIZATION_TOKEN']
                    }
                )
                print(milobella_response.text)
                print(milobella_response.json()["vocal"])
                talk(milobella_response.json()["vocal"])
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            finally:
                listening = False


except KeyboardInterrupt:
    print("Stopping....")

finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if sound is not None:
        sound.terminate()
