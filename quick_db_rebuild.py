"""
Simple Database Rebuild Script - Windows Compatible
"""
import os
import shutil
import chromadb
from chromadb.config import Settings

def rebuild_database():
    """Quick database rebuild to fix version mismatch"""
    print("Rebuilding North Indian RAG Database...")
    
    # Remove old database
    db_path = "./north_indian_rag_db"
    if os.path.exists(db_path):
        print("Removing old database...")
        shutil.rmtree(db_path)
    
    # Create new database with current ChromaDB version
    print("Creating new database...")
    client = chromadb.PersistentClient(
        path=db_path,
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Create collections (empty for now)
    recipes = client.get_or_create_collection("north_indian_recipes")
    ingredients = client.get_or_create_collection("ingredient_usage") 
    general = client.get_or_create_collection("general_food_search")
    
    print("Database structure created!")
    print(f"Collections created: {len(client.list_collections())}")
    
    print("NOTE: Database is empty. To populate with data, run the full build script.")
    return True

if __name__ == "__main__":
    rebuild_database()
