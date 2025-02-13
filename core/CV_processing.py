def load_resume(file_path):
    """Load the resume text from a file."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()


def generate_embedding(text, model):
    """Generate sentence embeddings for the given text."""
    return model.encode(text, convert_to_tensor=True)