"""
Quick script to check what collections exist in the ChromaDB
"""
import chromadb
import os

def check_collections():
    db_path = "./north_indian_rag_db"
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    try:
        client = chromadb.PersistentClient(path=db_path)
        collections = client.list_collections()
        
        print("Available collections:")
        for collection in collections:
            print(f"- {collection.name} (count: {collection.count()})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_collections()
