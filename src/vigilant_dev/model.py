from transformers import DistilBertModel, DistilBertTokenizer
import torch

# Load pre-trained DistilBERT model and tokenizer
model_name = 'distilbert-base-uncased'
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertModel.from_pretrained(model_name)

def text_to_vector(text):
    """
    Function to convert text to a vector using DistilBERT.
    """
    # Tokenize the text
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)

    # Get the embeddings
    with torch.no_grad():
        outputs = model(**inputs)

    # Mean of all token embeddings to represent the sentence
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()

    return embeddings
