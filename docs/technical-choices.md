# Technical choices
### Audio device
For now, I'm using a Raspberry PI 3B+ combined with a [RASPIAUDIO Ultra +](https://raspiaudio.com/produit/ultra).
It's onboard mic and speaker which is convenient for my experimentation.

### Wake up word
To trigger the discussion a "wake-up-word" technology is necessary. There is a lot of these technologies in the opensource world.
Here is the list of technologies experimented :
- [pocketsphinx](https://github.com/cmusphinx/pocketsphinx)
- [porcupine](https://github.com/Picovoice/porcupine)

[Wake up word experimentation](docs/wake-up-word-experimentation.md)

### Speech-To-Text
The translation of voice records into text is currently performed by the [Google Cloud Speech-To-Text API](https://cloud.google.com/speech-to-text).

The [mozilla/deepspeech](https://github.com/mozilla/DeepSpeech) project with Common Voice database is considered.

### Text-To-Speech
The translation of Milobella text answers into speech synthesis is ensured by [Google Cloud Text-To-Speech API](https://cloud.google.com/text-to-speech).

No replacement has been considered for now.
