import json
import time
from openai import OpenAI
from flask import current_app
from app.utils.caching import cache_result

client = OpenAI()

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


@cache_result(expire_seconds=86400)  # Cache for 24 hours
def translate_to_korean(text):
    """Translates English text to Korean using OpenAI with structured output."""
    if not text or len(text.strip()) == 0:
        raise ValueError("Empty text provided for translation")

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful translator. Translate the given English text to Korean. Respond with a JSON object containing a single key 'korean_translation' with the translated text as the value.",
                    },
                    {"role": "user", "content": text},
                ],
                temperature=0.3,
                max_tokens=150,
            )

            response_content = response.choices[0].message.content
            translation_data = json.loads(response_content)
            translation = translation_data.get("korean_translation")

            if not translation:
                current_app.logger.error(
                    f"Translation missing from response: {response_content}"
                )
                raise ValueError("Translation missing from API response")

            return translation

        except json.JSONDecodeError as e:
            current_app.logger.error(
                f"JSON decode error: {e}, Response: {response_content if 'response_content' in locals() else 'N/A'}"
            )
            if attempt == MAX_RETRIES - 1:
                raise
        except Exception as e:
            current_app.logger.error(
                f"Translation error (attempt {attempt + 1}/{MAX_RETRIES}): {e}"
            )
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(RETRY_DELAY)

    raise RuntimeError("Failed to translate after maximum retries")
