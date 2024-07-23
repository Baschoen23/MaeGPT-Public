import os
from openai import OpenAI
from recordAudio import audioRecorder
from config import API_KEY
import openai
import asyncio
from concurrent.futures import ThreadPoolExecutor
#from recordAudio import record_audio
#executor = ThreadPoolExecutor(max_workers=1)

client = OpenAI(api_key=API_KEY)

def speech_to_text(buttonState):#update_ui):
    audioReturner = audioRecorder()#update_ui)
    print("speech_to_text started")
    while buttonState:
        print("Recording")
        audioReturner.record_audio()#update_ui)
        #record_audio()
    print("Audio Saved")
    current_dir = os.getcwd()
    audio_file = open(current_dir + "\output.wav", "rb")
    print("Audio File Opened")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    print("Audio Transcribed")
    #print(transcript)
    return transcript



def call_voice_input():
    print("call_voice_input started")
    transcription = speech_to_text()
    print("Transcription finished")
    return transcription


