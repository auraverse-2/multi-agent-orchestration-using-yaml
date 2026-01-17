import chromadb
import uuid

class VectorDB:
    def __init__(self, collection_name="agent_knowledge_base"):
        print(f"🔌 Initializing Vector Database (In-Memory): {collection_name}")
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(self, text, source_agent_id, metadata={}):
        chunks = [c.strip() for c in text.split("\n") if c.strip()]
        
        if not chunks:
            return
        ids = [f"{source_agent_id}_{uuid.uuid4().hex[:8]}" for _ in chunks]
        
        base_metadata = {"author": source_agent_id, **metadata}
        metadatas = [base_metadata for _ in chunks]

        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        print(f"💾 [VectorDB] Saved to memory: {text[:30]}...")

    def search(self, query_text, n_results=1):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        if not results['documents'] or not results['documents'][0]:
            return None
        return results['documents'][0][0]
