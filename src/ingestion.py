"""
This module handles the ingestion of knowledge from various sources
into the ChromaDB knowledge base.
"""
from src.knowledge import KnowledgeBase
import os

def ingest_text_file(knowledge_base: KnowledgeBase, file_path: str):
    """
    Simulates scraping and ingesting knowledge from a text file.
    Each line in the file is treated as a separate document.

    Args:
        knowledge_base (KnowledgeBase): The knowledge base to ingest into.
        file_path (str): The path to the text file.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                doc_id = f"{os.path.basename(file_path)}-line-{i+1}"
                metadata = {"source": os.path.basename(file_path)}
                knowledge_base.add_document(line, metadata, doc_id)
    print(f"Successfully ingested {file_path}")