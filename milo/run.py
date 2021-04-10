#!/usr/bin/env python3
import speech_recognition as sr

from milo.milobella import Milobella
from milo.stt.__interface__ import STTInterface
from milo.tts.__interface__ import TTSInterface
from milo.wuw.__interface__ import WUWInterface


def run(milobella_url: str, tts: TTSInterface, wuw: WUWInterface, stt: STTInterface) -> None:
    milobella = Milobella(milobella_url)

    try:
        tts.synthesize_speech("Je suis prête")
        stt.prepare()
        listening = False

        while True:
            if wuw.process():
                listening = True

            if listening:
                try:
                    print("Oui ?")
                    question = stt.process()
                    print("Question : {}".format(question))
                    answer = milobella.milobella_request(question)
                    print("Answer : {}".format(answer))
                    tts.synthesize_speech(answer)
                except sr.UnknownValueError:
                    print("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    listening = False

    except KeyboardInterrupt:
        print("Stopping....")

    finally:
        wuw.terminate()
