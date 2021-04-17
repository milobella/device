from pocketsphinx import Pocketsphinx
import pyaudio

from milo.wuw.__interface__ import WUWInterface

_FRAME_LENGTH = 2048
_SAMPLE_RATE = 16000


class PocketSphinxWUW(WUWInterface):

    def __init__(self, keyword: str, kws_threshold: float):
        self._decoder = Pocketsphinx(keyphrase=keyword, lm=False, kws_threshold=kws_threshold)
        self._sound = pyaudio.PyAudio()
        self._audio_stream = self._sound.open(
            rate=_SAMPLE_RATE,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=_FRAME_LENGTH)

    def prepare(self) -> None:
        print("starting utterance")
        self._decoder.start_utt()
        print("started utterance")

    def process(self) -> bool:
        buf = self._audio_stream.read(_FRAME_LENGTH)
        if buf:
            self._decoder.process_raw(buf, False, False)
        else:
            return False

        if self._decoder.hyp():
            print(self._decoder.hyp().hypstr)
            # print([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in self._decoder.seg()])
            # print("Detected keyphrase, restarting search")
            # for best, i in zip(self._decoder.nbest(), range(10)):
            #     print(best.hypstr, best.score)
            print("ending utterance")
            self._decoder.end_utt()
            print("ended utterance")
            return True
        return False

    def terminate(self) -> None:
        if self._audio_stream is not None:
            self._audio_stream.close()

        if self._sound is not None:
            self._sound.terminate()
