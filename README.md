# musical-guide
A web app to be used as part of a study on evaluation metrics for generative machine learning models for music within an interaction context.

## Dependencies
This app was built using the following:
- Python 3.5.4
- Django 2.0.4
- Tensorflow 1.3.0
- [Magenta](https://github.com/tensorflow/magenta#installation)

It may work with other versions of these, but no guarantees.

## Demos (no sound)
URL to mp4 demo of web app (no sound included):
https://drive.google.com/file/d/1NziPgLeWwrcIuzI5EGW-GU8V4Qeaz5MB/view?usp=sharing

URL to gif demo of web app (no sound included):
https://drive.google.com/file/d/1ABW3FUXf38XJKmjoAJAO5BFrA5c-t4kd/view?usp=sharing

## Running the app
- Install dependencies
- Clone the repository
- Navigate to musical-guide/musicalguide/study/static/study and create a folder called audio containing all sound files in the required format, or copy and paste a folder of audio samples in to this location. If you skip this step, not sound or responses will occur in the interactions.
- In the command line, navigate back up to musical-guide/musicalguide
- Run python3 manage.py runserver 0.0.0.0:8000
- Open 127.0.0.1:8000/study in your browser

## Notes
- The audio files have been excluded. To run the server, an audio folder needs to be placed under musicalguide/study/static/study containing mp3 audio files named as 'noteName.mp3'. E.g. 'C4.mp3' for a C4 audio sample, or 'Cs4.mp3' for a C#4 audio sample. Will need audio samples for all notes C3 through B6.
- Only tested with Google Chrome on Mac and Windows
- Does not currently work with touchscreen
