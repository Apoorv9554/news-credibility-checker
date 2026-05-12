import re

def clean_input_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)
    text = text.replace('"', '').replace("'", "")
    text = re.sub(r"\s+", " ", text)

    return text.strip()
