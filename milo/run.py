#!/usr/bin/env python3
import speech_recognition as sr

from opentelemetry import trace
from opentelemetry import context
from opentelemetry.trace.propagation import _SPAN_KEY

from milo.message import print_info, print_warn
from milo.milobella import Milobella
from milo.stt.__interface__ import STTInterface
from milo.tts.__interface__ import TTSInterface
from milo.wuw.__interface__ import WUWInterface, WUWFeedbackInterface

_REQUEST_SPAN = "Request"


def run(milobella: Milobella,
        tts: TTSInterface,
        wuw: WUWInterface,
        stt: STTInterface,
        wuw_feedback: WUWFeedbackInterface) -> None:
    tracer = trace.get_tracer(__name__)

    try:
        tts.synthesize_speech("Je suis prête")
        stt.prepare()
        listening = False
        reprompt = False

        span = tracer.start_span(_REQUEST_SPAN)
        token = context.attach(context.set_value(_SPAN_KEY, span))

        wuw.prepare()

        while True:

            if not listening:
                if wuw.process():
                    wuw_feedback.start_listening_feedback()
                    listening = True

            if listening:
                try:
                    print_info("Oui ?")
                    question = stt.process()
                    print_info("Question : {}".format(question))
                    # scope.("question", question)
                    answer, reprompt = milobella.milobella_request(question)
                    # scope.set_attribute("answer", answer)
                    print_info("Réponse : {}".format(answer))
                    tts.synthesize_speech(answer)
                except sr.UnknownValueError:
                    print_warn("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print_warn("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    wuw_feedback.end_listening_feedback()
                    listening = False

                    span.end()
                    context.detach(token)
                    span = tracer.start_span(_REQUEST_SPAN)
                    token = context.attach(context.set_value(_SPAN_KEY, span))

                    if reprompt:
                        wuw_feedback.start_listening_feedback()
                        listening = True
                    else:
                        wuw.prepare()

    except KeyboardInterrupt:
        print_info("Stopping....")

    finally:
        wuw.terminate()
        wuw_feedback.terminate()
