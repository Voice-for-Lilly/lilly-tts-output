from flask import Flask, request
import os
from elevenlabs_api import generate_speech_elevenlabs
from coqui_tts_api import synthesize_audio_file
from pydub import AudioSegment
import pyaudio

app = Flask(__name__)

# Define the supported sample rate
SUPPORTED_SAMPLE_RATE = 48000

def play_audio(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    
    # Resample if necessary
    if audio.frame_rate != SUPPORTED_SAMPLE_RATE:
        audio = audio.set_frame_rate(SUPPORTED_SAMPLE_RATE)
    
    pyaudio_playback(audio)

def pyaudio_playback(audio_segment):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open the audio stream
    stream = p.open(format=p.get_format_from_width(audio_segment.sample_width),
                    channels=audio_segment.channels,
                    rate=audio_segment.frame_rate,
                    output=True,
                    output_device_index=find_usb_soundcard_index(p))

    # Play the audio
    stream.write(audio_segment.raw_data)
    stream.stop_stream()
    stream.close()
    p.terminate()

def find_usb_soundcard_index(p):
    card = 1  # Replace with your actual card number
    device = 0  # Replace with your actual device number
    
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(info.get('name', ''))
        if f"hw:{card},{device}" in info.get('name', ''):
            print(f"Found USB soundcard at index {i}")
            return i
        elif "USB Audio Device" in info.get('name', ''):
            print(f"Found USB soundcard at index {i}")
            return i
    raise ValueError("USB soundcard not found")

def get_audio_file(text):
    audio_file = synthesize_audio_file("tmp2.wav", text)
    play_audio(audio_file)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text")
    if not text:
        return {"error": "No text provided"}, 400    
    get_audio_file(text)    

    return {
        "status": "Audio played successfully"
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5011)