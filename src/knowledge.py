"""
This module manages all interactions with the ChromaDB knowledge base.
"""
import chromadb

class KnowledgeBase:
    """
    A wrapper for the ChromaDB client to manage the agent's knowledge.
    Uses an ephemeral client for in-memory, non-persistent storage.
    """
    def __init__(self, collection_name="agent_knowledge"):
        """
        Initializes the ChromaDB ephemeral client.

        Args:
            collection_name (str): The name of the collection to use.
        """
        self.client = chromadb.EphemeralClient()
        self.collection = self.client.get_or_create_collection(name=collection_name)

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