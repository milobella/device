#!/usr/bin/env python3
import speech_recognition as sr

from milo.message import print_info, print_warn
from milo.milobella import Milobella
from milo.stt.__interface__ import STTInterface
from milo.tts.__interface__ import TTSInterface
from milo.wuw.__interface__ import WUWInterface, WUWFeedbackInterface


def run(milobella: Milobella,
        tts: TTSInterface,
        wuw: WUWInterface,
        stt: STTInterface,
        wuw_feedback: WUWFeedbackInterface) -> None:
    try:
        tts.synthesize_speech("Je suis prête")
        stt.prepare()
        listening = False

        wuw.prepare()

        while True:
            if wuw.process():
                wuw_feedback.start_listening_feedback()
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
                    wuw_feedback.end_listening_feedback()
                    listening = False
                    wuw.prepare()

    except KeyboardInterrupt:
        print_info("Stopping....")

    finally:
        wuw.terminate()
        wuw_feedback.terminate()
