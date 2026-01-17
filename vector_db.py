# In vector_db.py (Compatibility version for 0.3.23)
import chromadb
from chromadb.config import Settings

class VectorDB:
    def __init__(self):
        # 0.3.23 uses Settings instead of PersistentClient
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        self.collection = self.client.get_or_create_collection(name="agent_knowledge")

    def add(self, text, source_agent_id):
        # Basic add function for 0.3.23
        self.collection.add(
            documents=[text],
            metadatas=[{"source": source_agent_id}],
            ids=[f"id_{hash(text)}"]
        )

    def search(self, query):
        results = self.collection.query(query_texts=[query], n_results=1)
        return results['documents'][0] if results['documents'] else ["No matching data found."]