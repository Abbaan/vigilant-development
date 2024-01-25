import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

def clean_text(text):
    """
    Function to clean text data.
    """
    # Remove unwanted characters and symbols
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)  # Keep only alphanumeric characters
    text = text.strip().lower()
    return text

def process_data(description):
    # Processing logic
    cleaned_description = clean_text(description)
    return cleaned_description


# Ensure you have the necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def extract_topics(descriptions):
    stopwords_set = set(stopwords.words('english'))
    all_words = []

    for desc in descriptions:
        # Tokenize and filter stopwords
        words = word_tokenize(desc)
        words = [word.lower() for word in words if word.isalpha()]
        words = [word for word in words if word not in stopwords_set]
        all_words.extend(words)

    # Get the most common words
    most_common = Counter(all_words).most_common(2)
    return ' / '.join(word for word, _ in most_common)

