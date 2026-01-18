import chromadb
import uuid
import os
from logger import log

class VectorDB:
    def __init__(self, session_id=None):
        # 1. Generate a unique ID if one isn't provided
        if session_id is None:
            session_id = str(uuid.uuid4())[:8] # Short unique ID
            
        # 2. Define a unique path for this instance
        self.persist_path = f"./chroma_db/{session_id}"
        
        # 3. Create the unique client
        self.client = chromadb.PersistentClient(path=self.persist_path)
        self.collection = self.client.get_or_create_collection(name="agent_knowledge")
        
        print(f"Initialized new Chroma instance at: {self.persist_path}")

    def add(self, text, source_agent_id):
        self.collection.add(
            documents=[text],
            metadatas=[{"source": source_agent_id}],
            ids=[str(uuid.uuid4())]
        )

    def search(self, query):
        results = self.collection.query(query_texts=[query], n_results=1)
        if results['documents'] and len(results['documents'][0]) > 0:
            log("FETCHED FROM DB", results['documents'][0])
            return results['documents'][0]
        return ["No matching data found."]
