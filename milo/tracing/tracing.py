from opentelemetry import trace

from milo.stt.__interface__ import STTInterface
from milo.tts.__interface__ import TTSInterface
from milo.wuw.__interface__ import WUWInterface, WUWFeedbackInterface


class WithTracingSTT(STTInterface):
    def __init__(self, decorated: STTInterface):
        self._dec = decorated
        self.tracer = trace.get_tracer(__name__)

    def prepare(self) -> None:
        with self.tracer.start_span('STT : Preparation'):
            return self._dec.prepare()

    def process(self) -> str:
        with self.tracer.start_span('STT : Processing'):
            return self._dec.process()


class WithTracingTTS(TTSInterface):
    def __init__(self, decorated: TTSInterface):
        self._dec = decorated
        self.tracer = trace.get_tracer(__name__)

    def synthesize_speech(self, text: str) -> None:
        with self.tracer.start_span('TTS : Synthesize Speech'):
            return self._dec.synthesize_speech(text)


class WithTracingWUW(WUWInterface):
    def __init__(self, decorated: WUWInterface):
        self._dec = decorated
        self.tracer = trace.get_tracer(__name__)

    def prepare(self) -> None:
        with self.tracer.start_span('WUW : Preparation'):
            return self._dec.prepare()

    def process(self) -> bool:
        with self.tracer.start_span('WUW : Processing'):
            return self._dec.process()

    def terminate(self) -> None:
        with self.tracer.start_span('WUW : Termination'):
            return self._dec.terminate()


class WithTracingWUWFeedback(WUWInterface):
    def __init__(self, decorated: WUWFeedbackInterface):
        self.tracer = trace.get_tracer(__name__)
        self._dec = decorated

    def start_listening_feedback(self):
        with self.tracer.start_span('WUW Feedback : Feedback the listening start'):
            return self._dec.start_listening_feedback()

    def end_listening_feedback(self):
        with self.tracer.start_span('WUW Feedback : Feedback the listening end'):
            return self._dec.end_listening_feedback()

    def terminate(self):
        with self.tracer.start_span('WUW Feedback : Terminate'):
            return self._dec.terminate()

