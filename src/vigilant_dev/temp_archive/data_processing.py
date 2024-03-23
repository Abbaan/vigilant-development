import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
import os
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


def markdown_files_to_df(folder_path):
    """
    Reads Markdown files from a specified folder, extracts the main title,
    description, and the Markdown link, compiling this information into
    a pandas DataFrame.

    Parameters:
    - folder_path: str, the path to the folder containing the Markdown files.

    Returns:
    - df: pandas.DataFrame, a DataFrame with columns for title, description, and link.
    """
    # Initialize an empty list to store the data
    data = []

    # Regular expressions to match the main title, description, and Markdown link
    title_pattern = re.compile(r'^##\s*(.*?)\s*$', re.MULTILINE)
    description_pattern = re.compile(r'^###\s*Description:\s*\n(.*)', re.MULTILINE)
    link_pattern = re.compile(r'\[Link\]\((.*?)\)', re.MULTILINE)

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Search for the main title, description, and Markdown link
                title_match = title_pattern.search(content)
                description_match = description_pattern.search(content)
                link_match = link_pattern.search(content)
                
                # Extract the main title, description, and the Markdown link URL
                title = title_match.group(1) if title_match else 'No Title Found'
                description = description_match.group(1) if description_match else 'No Description Found'
                link = link_match.group(1) if link_match else 'No Link Found'
                
                # Append the extracted data to the list
                data.append({'title': title, 'description': description, 'link': link, 'filename': filename})

    # Create a DataFrame from the list
    df = pd.DataFrame(data)
    return df

