import re

def clean_input_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace('"', '').replace("'", "")
    text = re.sub(r"\s+", " ", text)

    return text.strip()