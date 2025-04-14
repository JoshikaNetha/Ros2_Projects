import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal

import pyaudio
import json
import sounddevice as sd 
import wave


from core.config import settings

class VoiceRecorder(QThread):
    voice_signal = pyqtSignal(bytes)  # Signal to send text to another class

    def __init__(self):
        super().__init__()
        self.is_listening = False
        self.audio =        pyaudio.PyAudio()
        self.stream =       None
        self.frames =       []  # Store received audio data
        self.format =       pyaudio.paInt16

    def run(self):
        """Runs the recording loop in a separate thread"""

        self.stream = self.audio.open(format=self.format, channels=settings.VOICE_CHANNELS, rate=settings.VOICE_SAMPLE_RATE, input=True, frames_per_buffer=settings.VOICE_CHUNK)
        
        self.is_listening = True
        while self.is_listening:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                self.frames.append(data)
                self.voice_signal.emit(data)  # Emit signal with audio data
            except Exception as e:
                print(f"Audio Stream Error: {e}")  # Catch errors

        if self.frames:
            wave_filename = "received_audio.wav"
            try:
                wf = wave.open(wave_filename, 'wb')
                wf.setnchannels(settings.VOICE_CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.format))  # FIXED
                wf.setframerate(settings.VOICE_SAMPLE_RATE)
                wf.writeframes(b''.join(self.frames))
                wf.close()
                print(f"Audio saved as {wave_filename}")
            except Exception as e:
                print(f"Error saving audio: {e}")


   
    def stop(self):
        """Stop recording"""
        self.is_listening = False
        self.stream.stop_stream()
        self.audio.terminate()
        self.stream.close()