from __future__ import division

import io
import os
import json
import requests as requests_pkg
import pyaudio
from pydub import AudioSegment
from pydub.playback import play

from six import moves
from google.cloud import speech, texttospeech
from pocketsphinx import LiveSpeech

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class PlayClient():

    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()

        # Build the voice request
        # noinspection PyTypeChecker
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="fr-FR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        # Select the type of audio file you want returned
        # noinspection PyTypeChecker
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def synthesize_speech(self, text):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )

        play(AudioSegment.from_file(io.BytesIO(response.audio_content), format="mp3"))


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = moves.queue.Queue()
        self.closed = True

        self._audio_interface = pyaudio.PyAudio()
        # for i in range(self._audio_interface.get_device_count()):
        #     print(self._audio_interface.get_device_info_by_index(i))

    def __enter__(self):
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def terminate(self):
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except moves.queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(client: PlayClient, responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print("Finished: {}".format(result.is_final))
            print("Stability: {}".format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print("Confidence: {}".format(alternative.confidence))
                print(u"Transcript: {}".format(alternative.transcript))

            if result.is_final:
                milobella_response = requests_pkg.post(
                    'https://milobella.com:10443/talk/text',
                    data=json.dumps({'text': result.alternatives[0].transcript}),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + os.environ['MILOBELLA_AUTHORIZATION_TOKEN']
                    }
                )
                print(milobella_response.text)
                print(milobella_response.json()["vocal"])

                client.synthesize_speech(milobella_response.json()["vocal"])

                return


def main():

    sphinx_speech = LiveSpeech(keyphrase='bella', lm=False, kws_threshold=1e-20)

    client = speech.SpeechClient()
    play_client = PlayClient()

    # noinspection PyTypeChecker
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="fr-FR",
    )

    # noinspection PyTypeChecker
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    for _ in sphinx_speech:
        print("Started listening...")

        stream = MicrophoneStream(RATE, CHUNK)

        with stream:
            # Listen audio
            # noinspection PyTypeChecker
            requests = (
                speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream.generator()
            )

            # [START speech_python_migration_streaming_response]
            responses = client.streaming_recognize(
                config=streaming_config,
                requests=requests,
            )
            # [END speech_python_migration_streaming_request]

            # Now, put the transcription responses to use.
            listen_print_loop(play_client, responses)
            print("Stopped listening.")


if __name__ == '__main__':
    main()
