"""
North Indian RAG Vector Database Builder
Creates vector database from clean recipe/ingredient data for semantic search

SYSTEM ARCHITECTURE:
1. Loads clean JSON data (recipes + ingredients)
2. Converts text to embeddings using sentence-transformers
3. Stores vectors in ChromaDB for fast similarity search
4. Enables queries like "What's in Chole Bhature?" → ingredient lists

Requirements:
pip install chromadb sentence-transformers numpy pandas
"""

import json
import os
import time
from typing import List, Dict, Tuple, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

class NorthIndianRAGVectorDB:
    def __init__(self, data_file: str, db_path: str = "./rag_vector_db"):
        """
        Initialize RAG Vector Database Builder
        
        Args:
            data_file: Path to clean_north_indian_rag_data.json
            db_path: Directory to store ChromaDB database
        """
        self.data_file = data_file
        self.db_path = db_path
        self.embedding_model = None
        self.chroma_client = None
        self.collections = {}
        
        print("🏗️  Initializing North Indian RAG Vector Database")
        print(f"📊  Data source: {data_file}")
        print(f"💾  Database path: {db_path}")
        
    def load_clean_data(self) -> Dict:
        """Load the clean processed JSON data"""
        print("\n📖 Loading clean recipe data...")
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Data loaded successfully:")
            print(f"   • Recipes: {data['metadata']['total_recipes']}")
            print(f"   • RAG documents: {data['metadata']['total_rag_documents']}")
            print(f"   • Unique ingredients: {data['metadata']['total_unique_ingredients']}")
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def initialize_embedding_model(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize sentence transformer model for creating embeddings
        
        Args:
            model_name: HuggingFace model name (default optimized for speed/performance)
        """
        print(f"\n🧠 Loading embedding model: {model_name}")
        print("   This may take a moment on first run...")
        
        try:
            self.embedding_model = SentenceTransformer(model_name)
            
            # Test embedding to get dimensions
            test_embedding = self.embedding_model.encode("test recipe with ingredients")
            embedding_dim = len(test_embedding)
            
            print(f"✅ Embedding model ready:")
            print(f"   • Model: {model_name}")
            print(f"   • Embedding dimensions: {embedding_dim}")
            print(f"   • Device: {self.embedding_model.device}")
            
        except Exception as e:
            print(f"❌ Error loading embedding model: {e}")
            raise
    
    def initialize_vector_database(self, clean_start: bool = False):
        """Initialize ChromaDB vector database"""
        print(f"\n🗄️  Initializing ChromaDB database...")
        
        try:
            # Clean start option - remove existing database
            if clean_start and os.path.exists(self.db_path):
                print(f"   🧹 Cleaning existing database at {self.db_path}...")
                import shutil
                shutil.rmtree(self.db_path)
                print(f"   ✅ Old database removed")
            
            # Create database directory
            os.makedirs(self.db_path, exist_ok=True)
            
            # Initialize persistent ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=clean_start  # Allow reset only on clean start
                )
            )
            
            print(f"✅ ChromaDB initialized at: {self.db_path}")
            
        except Exception as e:
            print(f"❌ Error initializing ChromaDB: {e}")
            raise
    
    def create_collections(self):
        """Create specialized collections for different search types"""
        print("\n📚 Creating vector collections...")
        
        try:
            # Collection 1: Recipe-level search
            # Use case: "What's in Dal Makhani?" → Find recipe → Get all ingredients
            self.collections['recipes'] = self.chroma_client.get_or_create_collection(
                name="north_indian_recipes",
                metadata={
                    "description": "North Indian recipes with complete ingredient lists",
                    "search_type": "recipe_to_ingredients"
                }
            )
            
            # Collection 2: Ingredient-level search  
            # Use case: "Which dishes use paneer?" → Find ingredients → Get recipes
            self.collections['ingredients'] = self.chroma_client.get_or_create_collection(
                name="ingredient_usage",
                metadata={
                    "description": "Individual ingredient usage patterns in recipes",
                    "search_type": "ingredient_to_recipes"
                }
            )
            
            # Collection 3: General food search
            # Use case: "North Indian breakfast dishes" → Find by cuisine/course
            self.collections['general'] = self.chroma_client.get_or_create_collection(
                name="general_food_search",
                metadata={
                    "description": "General food and cuisine information",
                    "search_type": "general_food_queries"
                }
            )
            
            print(f"✅ Created {len(self.collections)} collections:")
            for name, collection in self.collections.items():
                print(f"   • {name}: {collection.name}")
                
        except Exception as e:
            print(f"❌ Error creating collections: {e}")
            raise
    
    def process_and_store_documents(self, data: Dict, batch_size: int = 20):
        """
        Process RAG documents and store in vector database
        
        Args:
            data: Clean recipe data from JSON
            batch_size: Number of documents to process at once
        """
        print(f"\n⚡ Processing and storing documents (batch size: {batch_size})...")
        
        rag_documents = data['rag_documents']
        total_docs = len(rag_documents)
        
        # Separate documents by type for different collections
        recipe_docs = [doc for doc in rag_documents if doc['type'] == 'recipe']
        ingredient_docs = [doc for doc in rag_documents if doc['type'] == 'ingredient_usage']
        
        print(f"📊 Document breakdown:")
        print(f"   • Recipe documents: {len(recipe_docs)}")
        print(f"   • Ingredient documents: {len(ingredient_docs)}")
        print(f"   • Total documents: {total_docs}")
        
        # Process recipe documents
        if recipe_docs:
            print(f"\n🍛 Processing recipe documents...")
            self._store_documents_batch(recipe_docs, 'recipes', batch_size)
        
        # Process ingredient documents  
        if ingredient_docs:
            print(f"\n🥬 Processing ingredient documents...")
            self._store_documents_batch(ingredient_docs, 'ingredients', batch_size)
        
        # Create general documents from recipes for broader search
        print(f"\n🔍 Creating general search documents...")
        general_docs = self._create_general_documents(data['recipes'])
        self._store_documents_batch(general_docs, 'general', batch_size)
        
        print(f"\n✅ All documents processed and stored!")
    
    def _store_documents_batch(self, documents: List[Dict], collection_name: str, batch_size: int):
        """Store documents in batches for memory efficiency with error recovery"""
        collection = self.collections[collection_name]
        total_docs = len(documents)
        successful_batches = 0
        
        for i in range(0, total_docs, batch_size):
            batch_end = min(i + batch_size, total_docs)
            batch = documents[i:batch_end]
            batch_num = i//batch_size + 1
            total_batches = (total_docs-1)//batch_size + 1
            
            print(f"   Processing batch {batch_num}/{total_batches} ({len(batch)} docs)...")
            
            try:
                # Extract text content and IDs
                texts = [doc['content'] for doc in batch]
                ids = [doc['id'] for doc in batch]
                metadatas = [doc['metadata'] for doc in batch]
                
                # Generate embeddings for this batch
                embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
                
                # Convert to list format for ChromaDB
                embeddings_list = embeddings.tolist()
                
                # Store in ChromaDB with retry logic
                max_retries = 3
                for retry in range(max_retries):
                    try:
                        collection.add(
                            documents=texts,
                            metadatas=metadatas,
                            embeddings=embeddings_list,
                            ids=ids
                        )
                        successful_batches += 1
                        break
                    except Exception as retry_error:
                        if retry < max_retries - 1:
                            print(f"     ⚠️ Retry {retry + 1}/{max_retries} for batch {batch_num}...")
                            time.sleep(2)  # Wait before retry
                        else:
                            raise retry_error
                
                # Longer delay between batches to prevent system overload
                time.sleep(0.5)
                
                # Checkpoint and memory cleanup every 25 batches
                if batch_num % 25 == 0:
                    print(f"     💾 Checkpoint: {batch_num} batches completed, forcing database persistence...")
                    try:
                        # Force ChromaDB to persist data
                        collection.persist() if hasattr(collection, 'persist') else None
                    except:
                        pass  # persist() might not be available in all ChromaDB versions
                    
                    print(f"     🧹 Memory cleanup after {batch_num} batches...")
                    import gc
                    gc.collect()
                    time.sleep(2)  # Longer pause for system recovery
                    
            except Exception as e:
                print(f"     ❌ Error in batch {batch_num}: {e}")
                print(f"     ⚠️ Continuing with next batch...")
                continue
        
        print(f"   ✅ Stored {successful_batches * batch_size} documents in '{collection_name}' collection")
        if successful_batches * batch_size < total_docs:
            print(f"   ⚠️ Warning: {total_docs - successful_batches * batch_size} documents may have failed to store")
    
    def _create_general_documents(self, recipes: List[Dict]) -> List[Dict]:
        """Create general search documents from recipes"""
        general_docs = []
        
        for recipe in recipes:
            # Create cuisine-focused document
            content = f"North Indian {recipe['course']} dish: {recipe['name']} from {recipe['cuisine']} cuisine. "
            content += f"Popular in North India, this {recipe['course']} contains {recipe['ingredient_count']} ingredients. "
            content += f"Typical ingredients: {', '.join(recipe['ingredients'][:5])}..."  # First 5 ingredients
            
            doc = {
                'id': f"general_{recipe['id']}",
                'type': 'general_info',
                'content': content,
                'metadata': {
                    'recipe_name': recipe['name'],
                    'cuisine': recipe['cuisine'],
                    'course': recipe['course'],
                    'region': recipe['region'],
                    'ingredient_count': recipe['ingredient_count'],
                    'source': recipe['source']
                }
            }
            general_docs.append(doc)
        
        return general_docs
    
    def create_search_functions(self):
        """Create optimized search functions for different query types"""
        print("\n🔍 Creating search functions...")
        
        def search_recipe_ingredients(query: str, n_results: int = 5) -> List[Dict]:
            """
            Search for recipes and return their ingredient lists
            Use case: "What's in Chole Bhature?" → ingredient list
            """
            try:
                results = self.collections['recipes'].query(
                    query_texts=[query],
                    n_results=n_results,
                    include=['documents', 'metadatas', 'distances']
                )
                
                formatted_results = []
                for i in range(len(results['documents'][0])):
                    result = {
                        'recipe_name': results['metadatas'][0][i]['recipe_name'],
                        'ingredients': results['metadatas'][0][i].get('all_ingredients', ''),
                        'cuisine': results['metadatas'][0][i]['cuisine'],
                        'course': results['metadatas'][0][i]['course'],
                        'confidence': 1 - results['distances'][0][i],  # Convert distance to confidence
                        'source': results['metadatas'][0][i]['source']
                    }
                    formatted_results.append(result)
                
                return formatted_results
                
            except Exception as e:
                print(f"Search error: {e}")
                return []
        
        def search_ingredient_usage(query: str, n_results: int = 10) -> List[Dict]:
            """
            Search for specific ingredient usage
            Use case: "Which dishes use paneer?" → recipe list
            """
            try:
                results = self.collections['ingredients'].query(
                    query_texts=[query],
                    n_results=n_results,
                    include=['documents', 'metadatas', 'distances']
                )
                
                formatted_results = []
                for i in range(len(results['documents'][0])):
                    result = {
                        'ingredient': results['metadatas'][0][i]['ingredient_name'],
                        'recipe_name': results['metadatas'][0][i]['recipe_name'],
                        'cuisine': results['metadatas'][0][i]['cuisine'],
                        'course': results['metadatas'][0][i]['course'],
                        'confidence': 1 - results['distances'][0][i],
                        'usage_context': results['documents'][0][i][:100] + "..."
                    }
                    formatted_results.append(result)
                
                return formatted_results
                
            except Exception as e:
                print(f"Search error: {e}")
                return []
        
        def search_general_food(query: str, n_results: int = 8) -> List[Dict]:
            """
            General food search across all collections
            Use case: "North Indian breakfast dishes" → general results
            """
            try:
                results = self.collections['general'].query(
                    query_texts=[query],
                    n_results=n_results,
                    include=['documents', 'metadatas', 'distances']
                )
                
                formatted_results = []
                for i in range(len(results['documents'][0])):
                    result = {
                        'recipe_name': results['metadatas'][0][i]['recipe_name'],
                        'cuisine': results['metadatas'][0][i]['cuisine'],
                        'course': results['metadatas'][0][i]['course'],
                        'confidence': 1 - results['distances'][0][i],
                        'description': results['documents'][0][i][:150] + "..."
                    }
                    formatted_results.append(result)
                
                return formatted_results
                
            except Exception as e:
                print(f"Search error: {e}")
                return []
        
        # Store search functions as instance methods
        self.search_recipe_ingredients = search_recipe_ingredients
        self.search_ingredient_usage = search_ingredient_usage  
        self.search_general_food = search_general_food
        
        print("✅ Search functions created:")
        print("   • search_recipe_ingredients() - Find ingredients in dishes")
        print("   • search_ingredient_usage() - Find dishes using specific ingredients")
        print("   • search_general_food() - General food queries")
    
    def verify_database(self):
        """Verify the vector database is working correctly"""
        print("\n🔬 Verifying vector database...")
        
        try:
            # Check collection counts
            for name, collection in self.collections.items():
                count = collection.count()
                print(f"   • {name}: {count} documents")
            
            # Test searches
            print("\n🧪 Testing search functions:")
            
            # Test 1: Recipe ingredient search
            test_results = self.search_recipe_ingredients("Chole Bhature", n_results=2)
            if test_results:
                print(f"   ✅ Recipe search: Found {len(test_results)} results")
                print(f"      Top result: {test_results[0]['recipe_name']}")
            else:
                print("   ⚠️  Recipe search: No results")
            
            # Test 2: Ingredient usage search
            test_results = self.search_ingredient_usage("paneer", n_results=2)
            if test_results:
                print(f"   ✅ Ingredient search: Found {len(test_results)} results")
                print(f"      Top result: {test_results[0]['recipe_name']}")
            else:
                print("   ⚠️  Ingredient search: No results")
            
            # Test 3: General search
            test_results = self.search_general_food("North Indian breakfast", n_results=2)
            if test_results:
                print(f"   ✅ General search: Found {len(test_results)} results")
                print(f"      Top result: {test_results[0]['recipe_name']}")
            else:
                print("   ⚠️  General search: No results")
            
            print("\n✅ Database verification complete!")
            
        except Exception as e:
            print(f"❌ Verification error: {e}")
            raise
    
    def build_complete_system(self):
        """Build the complete RAG vector database system"""
        print("=" * 80)
        print("🚀 BUILDING NORTH INDIAN RAG VECTOR DATABASE SYSTEM")
        print("=" * 80)
        
        start_time = time.time()
        
        try:
            # Step 1: Load data
            data = self.load_clean_data()
            
            # Step 2: Initialize embedding model
            self.initialize_embedding_model()
            
            # Step 3: Initialize vector database (with clean start)
            self.initialize_vector_database(clean_start=True)
            
            # Step 4: Create collections
            self.create_collections()
            
            # Step 5: Process and store documents
            self.process_and_store_documents(data)
            
            # Step 6: Create search functions
            self.create_search_functions()
            
            # Step 7: Verify system
            self.verify_database()
            
            # Calculate total time
            total_time = time.time() - start_time
            
            print("=" * 80)
            print("🎉 RAG VECTOR DATABASE BUILD COMPLETE!")
            print("=" * 80)
            print(f"⏱️  Total build time: {total_time:.1f} seconds")
            print(f"💾  Database location: {self.db_path}")
            print(f"🔍  Ready for ingredient queries!")
            print("\n📋 USAGE EXAMPLES:")
            print('   db.search_recipe_ingredients("What\'s in Dal Makhani?")')
            print('   db.search_ingredient_usage("Which dishes use paneer?")')
            print('   db.search_general_food("North Indian breakfast dishes")')
            print("=" * 80)
            
            return True
            
        except Exception as e:
            print(f"\n❌ BUILD FAILED: {e}")
            return False

# Usage and testing
def main():
    """Main function to build the RAG vector database"""
    
    # Configuration
    data_file = "clean_north_indian_rag_data.json"
    db_path = "./north_indian_rag_db"
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        print("Please run clean_process_indian_food.py first to generate the data file.")
        return False
    
    # Build the system
    rag_db = NorthIndianRAGVectorDB(data_file, db_path)
    success = rag_db.build_complete_system()
    
    if success:
        print("\n🎯 Your RAG system is ready!")
        print("Use the rag_db object to search for ingredients in North Indian dishes.")
        return rag_db
    else:
        print("\n💥 Build failed. Please check the errors above.")
        return None

if __name__ == "__main__":
    # Build the RAG vector database
    rag_system = main()
    
    if rag_system:
        # Interactive testing (optional)
        print("\n" + "="*50)
        print("🧪 INTERACTIVE TESTING")
        print("="*50)
        
        test_queries = [
            "What ingredients are in Chole Bhature?",
            "Dal Makhani ingredients",
            "Which dishes use paneer?",
            "North Indian breakfast dishes"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            if "ingredients" in query.lower() or "what" in query.lower():
                results = rag_system.search_recipe_ingredients(query, n_results=2)
                for result in results:
                    print(f"   📋 {result['recipe_name']}: {result['ingredients'][:100]}...")
            elif "which dishes" in query.lower():
                results = rag_system.search_ingredient_usage(query, n_results=3)
                for result in results:
                    print(f"   🍽️  {result['recipe_name']} uses {result['ingredient']}")
            else:
                results = rag_system.search_general_food(query, n_results=3)
                for result in results:
                    print(f"   🥘 {result['recipe_name']} ({result['course']})")
