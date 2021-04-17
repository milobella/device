#!/usr/bin/env python3
import speech_recognition as sr
import time

from milo.message import print_info, print_warn
from milo.milobella import Milobella
from milo.stt.__interface__ import STTInterface
from milo.tts.__interface__ import TTSInterface
from milo.wuw.__interface__ import WUWInterface


def run(milobella: Milobella, tts: TTSInterface, wuw: WUWInterface, stt: STTInterface) -> None:

    try:
        tts.synthesize_speech("Je suis prête")
        stt.prepare()
        listening = False

        wuw.prepare()

        while True:
            if wuw.process():
                listening = True

            if listening:
                try:
                    print_info("Oui ?")
                    question = stt.process()
                    print_info("Question : {}".format(question))
                    answer = milobella.milobella_request(question)
                    print_info("Réponse : {}".format(answer))
                    tts.synthesize_speech(answer)
                except sr.UnknownValueError:
                    print_warn("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print_warn("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    listening = False
                    # It seems to listen the extra end of the speak and triggers the WUW, so we make sure
                    # that the speech is fully finished before preparing the WUW
                    time.sleep(0.3)
                    wuw.prepare()

    except KeyboardInterrupt:
        print_info("Stopping....")

    finally:
        wuw.terminate()
