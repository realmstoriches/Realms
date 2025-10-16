"""
This module manages all interactions with the ChromaDB knowledge base.
"""
import chromadb

class KnowledgeBase:
    """
    A wrapper for the ChromaDB client to manage the agent's knowledge.
    """
    def __init__(self, path=":memory:"):
        """
        Initializes the ChromaDB client.

        Args:
            path (str): The path to the ChromaDB database. Defaults to in-memory.
        """
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("agent_knowledge")

    def add_document(self, document, metadata, doc_id):
        """
        Adds a document to the knowledge base.
        """
        self.collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def query(self, query_text, n_results=1):
        """
        Queries the knowledge base for relevant information.
        """
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )