import os
import argparse
import json  # Import json library
from openai import OpenAI
from dotenv import load_dotenv
import sys  # Import sys for stderr

# Define the output directory
OUTPUT_DIR = "audio_output"

# Load environment variables (especially OPENAI_API_KEY)
load_dotenv()

# Initialize OpenAI client
# It will automatically look for the OPENAI_API_KEY environment variable
client = OpenAI()


def translate_to_korean(text):
    """Translates English text to Korean using OpenAI with structured output."""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            response_format={"type": "json_object"},  # Request JSON output
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful translator. Translate the given English text to Korean. Respond with a JSON object containing a single key 'korean_translation' with the translated text as the value.",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.3,
            max_tokens=150,  # Increased slightly just in case
        )
        # Parse the JSON response
        response_content = response.choices[0].message.content
        translation_data = json.loads(response_content)
        translation = translation_data.get("korean_translation")

        if not translation:
            print(
                "Error: 'korean_translation' key not found in the response.",
                file=sys.stderr,
            )
            print(f"Raw response: {response_content}", file=sys.stderr)
            return None
        return translation
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from response: {response_content}",
            file=sys.stderr,
        )
        return None
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        return None


def text_to_speech(text, filename):
    """Converts text to speech using OpenAI TTS and saves as an MP3 file in the output directory using streaming."""
    try:
        # Ensure the output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Construct the full path
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Use OpenAI's TTS API with streaming response within a with block
        with client.audio.speech.with_streaming_response.create(
            model="tts-1", voice="onyx", input=text, response_format="mp3"
        ) as response:
            # Stream the audio data to the file using the method on the yielded response object
            response.stream_to_file(filepath)

        print(f"Audio saved to: {filepath}")
    except Exception as e:
        print(f"Error during OpenAI text-to-speech generation: {e}", file=sys.stderr)


def create_filename(text):
    """Creates a valid base filename (without directory) from the input text."""
    # Basic cleaning: lowercase, replace spaces with underscores, remove punctuation
    filename = text.lower().replace(" ", "_")
    filename = "".join(c for c in filename if c.isalnum() or c == "_")
    # Limit length
    filename = filename[:50]
    # Ensure filename is not empty after cleaning
    if not filename:
        filename = "output"
    return f"{filename}.mp3"


def main():
    parser = argparse.ArgumentParser(
        description="Translate English to Korean and generate audio."
    )
    parser.add_argument("phrase", nargs="?", help="The English phrase to translate.")
    args = parser.parse_args()

    if args.phrase:
        english_phrase = args.phrase
    else:
        english_phrase = input("Enter English phrase: ")

    korean_translation = translate_to_korean(english_phrase)

    if korean_translation:
        print(f"\nKorean: {korean_translation}")
        audio_filename = create_filename(english_phrase)
        text_to_speech(korean_translation, audio_filename)


if __name__ == "__main__":
    main()
