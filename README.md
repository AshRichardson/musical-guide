# musical-guide
A web app to be used as part of a study on evaluation metrics for generative machine learning models for music within an interaction context.

## Dependencies
This app was built using the following:
- Python 3.5.4
- Django 2.0.4
- Tensorflow 1.3.0
- [Magenta](https://github.com/tensorflow/magenta#installation)

It may work with other versions of these, but no guarantees.

## Notes
- The audio files have been excluded. To run the server, an audio folder needs to be placed under musicalguide/study/static/study containing mp3 audio files named as 'noteName.mp3'. E.g. 'C4.mp3' for a C4 audio sample, or 'Cs4.mp3' for a C#4 audio sample. Will need audio samples for all notes C3 through B6.
