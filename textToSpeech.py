from pathlib import Path
from openai import OpenAI
from playsound import playsound
#from playsound2 import playsound2
import os.path
from config import API_KEY


client = OpenAI(api_key=API_KEY)

def text_to_speech(text):
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text
  )
  print("Response obtained")
  response.stream_to_file("C:\\Users\\basch\\Desktop\\output_tts.mp3")

  # Play MP3 file

  normalized_path = os.path.normpath("C:\\Users\\basch\\Desktop\\output_tts.mp3")
  print("Playing MP3 file")
  playsound(normalized_path)

#text_to_speech("Hi there! I'm Mae! What can I do for you?")


'''
from pydub import AudioSegment
from pydub.playback import play


# Load your MP3 file
audio = AudioSegment.from_file("C:\\Users\\basch\Desktop\output_tts.mp3", format="mp3")

# Play the audio file
play(audio)
'''

'''
It looks like you're using the OpenAI API to generate speech content with their text-to-speech (TTS) model and attempting to save the resulting audio to an MP3 file. As of my knowledge cutoff date in March 2023, OpenAI provides this feature through their API, and your usage of the `response.stream_to_file("output.mp3")` method should be saving the MP3 file as you need.

Now, to play the output audio file in Python, you can use a library that handles audio playback, such as `pygame` or `playsound`. Below, you will find examples of how to play the audio file using both libraries.

If you want to use `pygame`, install it first with `pip`:

```bash
pip install pygame
```

And here's an example of how to play an MP3 file using `pygame`:

```python
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load your MP3 file
pygame.mixer.music.load("output.mp3")

# Play the loaded MP3 file
pygame.mixer.music.play()

# This loop keeps the program running until the music stops playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
```

Alternatively, the `playsound` module offers a straightforward way to play sound files. Install it with:

```bash
pip install playsound
```

And here's how to use `playsound`:

```python
from playsound import playsound

# Play your MP3 file
playsound("output.mp3")
```

Note that the `playsound` library plays the sound on the main thread and will block until the file is done playing. You cannot control the volume or check if the file is done playing without using additional threads or functionality.

Choose the library based on your project's needs. The `pygame` method is more versatile and allows for additional controls such as volume adjustments and better event handling, while the `playsound` library is sufficient for basic audio playbacks.'''