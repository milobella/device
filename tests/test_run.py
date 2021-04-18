import unittest
from unittest.mock import patch, Mock, call
from milo import run
from typing import cast


class TestRun(unittest.TestCase):
    @patch('milo.milobella.Milobella')
    @patch('milo.tts.__interface__.TTSInterface')
    @patch('milo.wuw.__interface__.WUWInterface')
    @patch('milo.stt.__interface__.STTInterface')
    @patch('milo.wuw.__interface__.WUWFeedbackInterface')
    def test_run(self, mock_milobella, mock_tts, mock_wuw, mock_stt, mock_wuw_fb):
        """
        Two wake up word triggered
        Two questions asked
        Two answers
        Interruption occurs during the last TTS
        :return:
        """
        milobella_instance = cast(Mock, mock_milobella.return_value)
        tts_instance = cast(Mock, mock_tts.return_value)
        wuw_instance = cast(Mock, mock_wuw.return_value)
        stt_instance = cast(Mock, mock_stt.return_value)
        wuw_fb_instance = cast(Mock, mock_wuw_fb.return_value)

        wuw_instance.process.side_effect = [True, True]
        stt_instance.process.side_effect = ["Salut", "Comment ça va"]
        milobella_instance.milobella_request.side_effect = ["Bonjour", "Ça va bien"]
        tts_instance.synthesize_speech.side_effect = [None, None, KeyboardInterrupt]

        run.run(milobella_instance, tts_instance, wuw_instance, stt_instance, wuw_fb_instance)

        tts_instance.synthesize_speech.assert_has_calls([call('Je suis prête'), call('Bonjour'), call('Ça va bien')])
        wuw_instance.prepare.assert_has_calls([call(), call()])
        stt_instance.prepare.assert_called_once()
        wuw_instance.process.assert_has_calls([call(), call()])
        stt_instance.process.assert_has_calls([call(), call()])
        milobella_instance.milobella_request.assert_has_calls([call("Salut"), call("Comment ça va")])
        self.assertRaises(KeyboardInterrupt)


if __name__ == '__main__':
    unittest.main()
