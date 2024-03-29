import re

def clean_text(text):
    """
    Function to clean text data.
    """
    # Remove unwanted characters and symbols
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)  # Keep only alphanumeric characters
    text = text.strip().lower()
    return text