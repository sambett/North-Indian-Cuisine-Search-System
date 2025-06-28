"""
Simple Data Loader - Load recipes into ChromaDB
"""
import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

def load_recipe_data():
    """Load recipe data into the database"""
    print("Loading North Indian recipe data...")
    
    # Load data
    with open('clean_north_indian_rag_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Found {len(data['recipes'])} recipes")
    print(f"Found {len(data['rag_documents'])} RAG documents")
    
    # Initialize embedding model
    print("Loading AI model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Connect to database
    client = chromadb.PersistentClient(
        path="./north_indian_rag_db",
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Get collections
    recipes_col = client.get_collection("north_indian_recipes")
    ingredients_col = client.get_collection("ingredient_usage")
    general_col = client.get_collection("general_food_search")
    
    # Process RAG documents
    rag_docs = data['rag_documents']
    
    # Separate by type
    recipe_docs = [doc for doc in rag_docs if doc['type'] == 'recipe']
    ingredient_docs = [doc for doc in rag_docs if doc['type'] == 'ingredient_usage']
    
    print(f"Processing {len(recipe_docs)} recipe documents...")
    
    # Load recipe documents (smaller batch)
    if recipe_docs:
        batch_size = 10
        for i in range(0, len(recipe_docs), batch_size):
            batch = recipe_docs[i:i+batch_size]
            print(f"  Loading batch {i//batch_size + 1}...")
            
            texts = [doc['content'] for doc in batch]
            ids = [doc['id'] for doc in batch] 
            metadatas = [doc['metadata'] for doc in batch]
            embeddings = model.encode(texts).tolist()
            
            recipes_col.add(
                documents=texts,
                metadatas=metadatas,
                embeddings=embeddings,
                ids=ids
            )
    
    print(f"Processing {len(ingredient_docs)} ingredient documents...")
    
    # Load ingredient documents (smaller batches)
    if ingredient_docs:
        batch_size = 50
        for i in range(0, min(1000, len(ingredient_docs)), batch_size):  # Load first 1000 for speed
            batch = ingredient_docs[i:i+batch_size]
            print(f"  Loading ingredient batch {i//batch_size + 1}...")
            
            texts = [doc['content'] for doc in batch]
            ids = [doc['id'] for doc in batch]
            metadatas = [doc['metadata'] for doc in batch]
            embeddings = model.encode(texts).tolist()
            
            ingredients_col.add(
                documents=texts,
                metadatas=metadatas, 
                embeddings=embeddings,
                ids=ids
            )
    
    # Create general documents from recipes
    print("Creating general search documents...")
    general_docs = []
    for recipe in data['recipes'][:100]:  # First 100 for speed
        content = f"North Indian {recipe['course']} dish: {recipe['name']} from {recipe['cuisine']} cuisine. "
        content += f"Contains {recipe['ingredient_count']} ingredients: {', '.join(recipe['ingredients'][:3])}..."
        
        general_docs.append({
            'id': f"general_{recipe['id']}",
            'content': content,
            'metadata': {
                'recipe_name': recipe['name'],
                'cuisine': recipe['cuisine'],
                'course': recipe['course'],
                'ingredient_count': recipe['ingredient_count']
            }
        })
    
    if general_docs:
        texts = [doc['content'] for doc in general_docs]
        ids = [doc['id'] for doc in general_docs]
        metadatas = [doc['metadata'] for doc in general_docs]
        embeddings = model.encode(texts).tolist()
        
        general_col.add(
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings, 
            ids=ids
        )
    
    print("Data loading complete!")
    print(f"  - Recipes: {recipes_col.count()} documents")
    print(f"  - Ingredients: {ingredients_col.count()} documents") 
    print(f"  - General: {general_col.count()} documents")
    
    return True

if __name__ == "__main__":
    load_recipe_data()
