from abc import ABC, abstractmethod 
from .data_structures.learning_resource import LearningResource, LearningResourceCollection
import pandas as pd
import re
import os


class DataExtractionStrategy(ABC):
    """Abstract base class for a extraction strategy."""
    
    def extract_elements(self) -> LearningResource:
        """Extract the elements from the learning resource."""
        pass



class HeadingBasedExtraction(DataExtractionStrategy):
    """Concrete implementation of an extraction strategy."""
    
    def extract_elements(self, file_path: str) -> LearningResource:
        """Extract the elements from the learning resource."""

        # Regular expressions to match the main title, description, and Markdown link
        title_pattern = re.compile(r'^##\s*(.*?)\s*$', re.MULTILINE)
        description_pattern = re.compile(r'^###\s*Description:\s*\n(.*)', re.MULTILINE)
        url_pattern = re.compile(r'\[Link\]\((.*?)\)', re.MULTILINE)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Search for the main title, description, and Markdown link
            title_match = title_pattern.search(content)
            description_match = description_pattern.search(content)
            url_match = url_pattern.search(content)
            
            # Extract the main title, description, and the Markdown link URL
            title = title_match.group(1) if title_match else 'No Title Found'
            description = description_match.group(1) if description_match else 'No Description Found'
            url = url_match.group(1) if url_match else 'No Link Found'
            
            return LearningResource(title=title, description=description, url=url)



class LearningResourceLoader():
    """Class to load in markdown files from a folder as LearningResources."""

    def __init__(self, folder_path: str, data_extraction_strategy: DataExtractionStrategy):
        self.folder_path = folder_path
        self.data_extraction_strategy = data_extraction_strategy

    def load_learning_resources(self) -> LearningResourceCollection:
        """Load the learning resources."""
        learning_resources = LearningResourceCollection(resources=[])

        # Loop through each file in the folder
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".md"):
                file_path = os.path.join(self.folder_path, filename)
                learning_resource = self.data_extraction_strategy.extract_elements(file_path)
                    
                # Append the extracted data to the list
                learning_resources.add_resource(learning_resource)

        return learning_resources

    
    





        

