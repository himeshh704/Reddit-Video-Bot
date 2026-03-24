import asyncio
import edge_tts
import os

# Good creepy/story voices: en-US-GuyNeural (male), en-GB-SoniaNeural (female, british), en-US-ChristopherNeural (male)
DEFAULT_VOICE = "en-US-GuyNeural"

async def async_generate_audio(text, output_file, voice=DEFAULT_VOICE):
    """
    Asynchronously generates TTS audio from text and saves to output_file.
    """
    print(f"Generating audio (Voice: {voice})...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"Audio saved to {output_file}")

def generate_audio(text, output_file, voice=DEFAULT_VOICE):
    """
    Synchronous wrapper for generating audio.
    """
    # Check if the output directory exists
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    
    asyncio.run(async_generate_audio(text, output_file, voice))

if __name__ == "__main__":
    # Test the audio generator
    test_text = "This is a test of the automatic text to speech generator for creepy stories on YouTube."
    output = "test_audio.mp3"
    generate_audio(test_text, output)
    print("Test complete.")
