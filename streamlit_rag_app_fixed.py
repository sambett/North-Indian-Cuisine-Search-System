"""
Fixed Streamlit App for Docker - handles path issues better
"""
import streamlit as st
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Multiple possible database paths for Docker
POSSIBLE_DB_PATHS = [
    "./north_indian_rag_db",
    "/app/north_indian_rag_db", 
    "north_indian_rag_db",
    "../north_indian_rag_db"
]

def find_database():
    """Find the database directory"""
    for path in POSSIBLE_DB_PATHS:
        if os.path.exists(path):
            return path
    return None

def check_collections(db_path):
    """Check what collections exist in the database"""
    try:
        client = chromadb.PersistentClient(path=db_path)
        collections = client.list_collections()
        return {col.name: col for col in collections}
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return {}

def main():
    st.title("🍛 North Indian Cuisine Search System")
    
    # Find database
    db_path = find_database()
    
    if not db_path:
        st.error("❌ Vector database not found!")
        st.info("Checked paths:")
        for path in POSSIBLE_DB_PATHS:
            st.info(f"  - {path}")
        
        # Debug info
        st.markdown("### 🔍 Debug Information")
        st.write("Current working directory:", os.getcwd())
        st.write("Directory contents:", os.listdir("."))
        return
    
    st.success(f"✅ Database found at: {db_path}")
    
    # Check collections
    collections = check_collections(db_path)
    
    if not collections:
        st.error("No collections found in database")
        return
    
    st.success(f"✅ Found {len(collections)} collections:")
    for name, collection in collections.items():
        st.write(f"  - {name}: {collection.count()} documents")
    
    # Initialize embedding model
    @st.cache_resource
    def load_model():
        return SentenceTransformer('all-MiniLM-L6-v2')
    
    model = load_model()
    st.success("✅ AI model loaded")
    
    # Simple search interface
    st.markdown("## 🔍 Search")
    
    collection_name = st.selectbox("Choose collection:", list(collections.keys()))
    query = st.text_input("Enter search query:", placeholder="e.g., Dal Makhani")
    
    if st.button("Search") and query:
        try:
            collection = collections[collection_name]
            results = collection.query(
                query_texts=[query],
                n_results=5,
                include=['documents', 'metadatas', 'distances']
            )
            
            st.markdown(f"### Results for '{query}':")
            
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0], 
                results['distances'][0]
            )):
                confidence = (1 - distance) * 100
                
                with st.expander(f"Result {i+1} (Confidence: {confidence:.1f}%)"):
                    st.write("**Content:**", doc[:300] + "..." if len(doc) > 300 else doc)
                    st.write("**Metadata:**", metadata)
                    
        except Exception as e:
            st.error(f"Search error: {e}")

if __name__ == "__main__":
    main()
