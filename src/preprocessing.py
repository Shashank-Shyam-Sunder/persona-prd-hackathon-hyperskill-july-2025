import re
import pandas as pd
from typing import List, Union

def clean_text(text: str) -> str:
    """
    Clean a single text string for NLP tasks.

    Returns:
        str: Cleaned text.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)                         # Remove URLs
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)                # Markdown links
    text = re.sub(r'[^a-z0-9\s.,;!?\'"-]', ' ', text)                   # Keep basic punctuation
    text = re.sub(r'\s+', ' ', text)                                    # Normalize whitespace
    return text.strip()

def preprocess_texts(texts: Union[List[str], pd.Series]) -> pd.Series:
    """
    Clean a list or Series of raw texts.

    Args:
        texts (list or pd.Series): Input texts

    Returns:
        pd.Series: Cleaned texts
    """
    texts = pd.Series(texts) if isinstance(texts, list) else texts
    return texts.apply(clean_text)

# Optional test case
if __name__ == "__main__":
    sample = [
        "Example with [link](http://example.com) and text.",
        "Visit http://google.com for more!",
        None,
        "Messy text!!! ###### $$$",
        "Multiline\nand    weird   spacing"
    ]
    cleaned = preprocess_texts(sample)
    for raw, cl in zip(sample, cleaned):
        print(f"\nOriginal: {raw}\nCleaned:  {cl}")
