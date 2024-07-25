import cTTS
import os

def synthesize_audio_file(temp_filename, text):
    cTTS.synthesizeToFile(temp_filename, text)
    
    return temp_filename

def delete_audio_file(filename):
    os.remove(filename)

    return True