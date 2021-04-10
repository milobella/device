import struct

import pvporcupine
import pyaudio

from milo.wuw.__interface__ import WUWInterface


class PorcupineWUW(WUWInterface):
    def __init__(self):
        self._porcupine = pvporcupine.create(keywords=["picovoice"])

        self._sound = pyaudio.PyAudio()

        self._audio_stream = self._sound.open(
            rate=self._porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self._porcupine.frame_length)

    def process(self) -> bool:
        pcm = self._audio_stream.read(self._porcupine.frame_length)
        pcm = struct.unpack_from("h" * self._porcupine.frame_length, pcm)

        return self._porcupine.process(pcm) >= 0

    def terminate(self) -> None:
        if self._porcupine is not None:
            self._porcupine.delete()

        if self._audio_stream is not None:
            self._audio_stream.close()

        if self._sound is not None:
            self._sound.terminate()
