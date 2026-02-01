# === Python Module ===
import re
import pandas as pd

# === Function to normalise text ===
def normalize_text(
        text: str
) -> str:
    ## === Changing text into lower characters ===
    text = text.lower()

    ## === Normalizing newlines (windows -> unix) ===
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    ## === Replace newlines with space ===
    text = re.sub(r"\n+", " ", text)

    ## === Collapse spaces & tabs ===
    text = re.sub(r"[ \t]+", " ", text)

    ## === Remove punctuation (keep alphanumerics + space) ===
    text = re.sub(r"[^a-z0-9 ]", "", text)

    ## === Returning text with removing side spaces ===
    return text.strip()

# === Creates Dedup key for a single article ===
def make_dedup_key(
        text: str,
        character_limit: int
) -> str:
    """
    Creates a stable dedup key from normalized content.
    """
    return text[:character_limit]

# === Gets the cleaned and dedup key for all the content ===
def get_content(
        data: pd.DataFrame,
        character_limit: int = 300
):
    """
    Gets the trimmed content for comparison
    """
    return data["content"].fillna("").apply(
        lambda x: make_dedup_key(x, character_limit)
    )