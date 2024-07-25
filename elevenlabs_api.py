from elevenlabs import generate, set_api_key

set_api_key("bbe1b03a0f186ce03b0d5d4a68fc5360")  # Replace with your actual API key


def generate_speech_elevenlabs(text, voice="Rachel", model="eleven_multilingual_v2"):
    audio = generate(
        text=text,
        voice=voice,
        model=model,
        latency=3
    )
    return audio


# Usage
# audio = generate_speech("Das ist ein Test für Lilly.")
# Optionally play the audio
# play(audio)
