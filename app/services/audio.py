import os
import time
from openai import OpenAI
from flask import current_app

client = OpenAI()

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def generate_audio(text, filepath):
    """Converts text to speech using OpenAI TTS and saves as an MP3 file."""
    if not text or len(text.strip()) == 0:
        raise ValueError("Empty text provided for audio generation")

    for attempt in range(MAX_RETRIES):
        try:
            with client.audio.speech.with_streaming_response.create(
                model="tts-1", voice="onyx", input=text, response_format="mp3"
            ) as response:
                response.stream_to_file(filepath)

            # Verify file was created and has content
            if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                raise IOError(f"Audio file was not created or is empty: {filepath}")

            return os.path.basename(filepath)

        except Exception as e:
            current_app.logger.error(
                f"Audio generation error (attempt {attempt + 1}/{MAX_RETRIES}): {e}"
            )
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(RETRY_DELAY)

    raise RuntimeError("Failed to generate audio after maximum retries")
