#!/usr/bin/env python3
import speech_recognition as sr
import struct
import pyaudio
import pvporcupine

from milo.google import talk
from milo.milobella import Milobella


def run_porcupine(milobella_url: str):
    r = sr.Recognizer()
    m = sr.Microphone()
    milobella = Milobella(milobella_url)

    porcupine = None
    sound = None
    audio_stream = None

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
                print("Déclenché")

            if listening:
                with m as source:
                    audio = r.listen(source)
                try:
                    print("Oui ?")
                    question = r.recognize_google(audio, language="fr-FR")
                    print("Question : {}".format(question))
                    answer = milobella.milobella_request(question)
                    print("Answer : {}".format(answer))
                    talk(answer)
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
