from milo.stt.__interface__ import STTInterface
import speech_recognition


class GoogleSTT(STTInterface):
    def __init__(self):
        self._recognizer = speech_recognition.Recognizer()
        self._microphone = speech_recognition.Microphone()

    def prepare(self) -> None:
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

    def process(self) -> str:
        with self._microphone as source:
            audio = self._recognizer.listen(source)
        return self._recognizer.recognize_google(audio, language="fr-FR")
