import streamlit as st
import speech_recognition as sr
import soundfile as sf
import time 
import tempfile
import re
import os
import numpy as np
from Api import CreateQuiz
def start():
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    st.write('Listening .........')

    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        audio_data = recognizer.record(mic, 5)
        st.write("Recording finished!")
        text = recognizer.recognize_google(audio_data)
    st.write('Transcription : '+text)
    st.write('here is the google form Link : '+CreateQuiz(text))


def main():
    st.title("Microphone Recorder")
    st.write("Click the button below to start.")
    if st.button('Start App'):
        st.write('Starting...')
        start()
        

if __name__ == "__main__":
    main()
