def validate_phrase(text):
    """Validate phrase for translation API"""
    if not text:
        return False, "Text cannot be empty"

    text = text.strip()
    if len(text) == 0:
        return False, "Text cannot be empty"

    if len(text) > 500:
        return False, "Text is too long (maximum 500 characters)"

    return True, ""
