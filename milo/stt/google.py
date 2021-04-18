from milo.stt.__interface__ import STTInterface
import speech_recognition
import pyaudio


class Microphone(speech_recognition.AudioSource):
    CHUNK = 2048
    SAMPLE_RATE = 16000

    # noinspection PyMissingConstructor
    def __init__(self):
        self._sound = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.SAMPLE_WIDTH = pyaudio.get_sample_size(self.format)
        self.stream = self._sound.open(
            rate=self.SAMPLE_RATE,
            channels=1,
            format=self.format,
            input=True,
            frames_per_buffer=self.CHUNK)

    def __enter__(self):
        self.stream.start_stream()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.stop_stream()


class GoogleSTT(STTInterface):
    def __init__(self):
        self._recognizer = speech_recognition.Recognizer()
        self._microphone = Microphone()

    def prepare(self) -> None:
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

    def process(self) -> str:
        print("before STT Mic initialization")
        with self._microphone as source:
            print("before STT audio listening")
            audio = self._recognizer.listen(source)
            print("after STT audio listening")
        print("after STT Mic destroy")
        return self._recognizer.recognize_google(audio, language="fr-FR")
