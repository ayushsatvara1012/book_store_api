from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(title: str, author: str):
    # Combining title and author creates a better "semantic context"
    text = f"Title: {title} Author: {author}"
    return model.encode(text).tolist()