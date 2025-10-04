

---



\## 📁 `chromadb\_docs.md`



```markdown

\# ChromaDB Overview



ChromaDB is a vector database optimized for embedding storage and retrieval. It powers semantic search, RAG pipelines, and agent memory.



\## Core Features



\- \*\*Collections\*\*: Logical groupings of embeddings.

\- \*\*Documents\*\*: Text chunks stored with metadata.

\- \*\*Embeddings\*\*: Vector representations of text.

\- \*\*Querying\*\*: Retrieve top-k matches based on similarity.



\## API Example



```python

import chromadb

from chromadb.config import Settings



client = chromadb.Client(Settings(persist\_directory="./vault"))

collection = client.get\_or\_create\_collection(name="agent\_ada")



collection.add(documents=\["Ada was a pioneer."], embeddings=\[\[0.1, 0.2, ...]], ids=\["ada\_1"])

results = collection.query(query\_embeddings=\[\[0.1, 0.2, ...]], n\_results=5)

