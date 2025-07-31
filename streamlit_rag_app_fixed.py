"""
Enhanced North Indian Cuisine RAG Search System
Beautiful, professional Streamlit interface with advanced features
Fixed for Streamlit Cloud deployment with ChromaDB compatibility
"""
import streamlit as st
import os
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="North Indian Cuisine Search",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ChromaDB import with error handling for Streamlit Cloud
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ ChromaDB import failed: {e}")
    st.info("This might be a Streamlit Cloud compatibility issue. Please check the requirements.txt file.")
    CHROMADB_AVAILABLE = False
    st.stop()

# Sentence Transformers import with error handling
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Sentence Transformers import failed: {e}")
    st.info("Please ensure sentence-transformers is properly installed.")
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    st.stop()

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
    }
    .search-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #FF6B35;
    }
    .confidence-high { border-left-color: #28a745; }
    .confidence-medium { border-left-color: #ffc107; }
    .confidence-low { border-left-color: #dc3545; }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
    }
    .error-container {
        background: #fee;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Database configuration with multiple fallback paths
POSSIBLE_DB_PATHS = [
    "./north_indian_rag_db",
    "/app/north_indian_rag_db", 
    "north_indian_rag_db",
    "../north_indian_rag_db",
    "/mount/src/north-indian-cuisine-search-system/north_indian_rag_db",  # Streamlit Cloud path
    "/mount/src/north-indian-cuisine-search-system/north_indian_rag_db/"   # Alternative
]

@st.cache_resource
def load_embedding_model():
    """Load and cache the embedding model with error handling"""
    try:
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        st.error(f"❌ Failed to load embedding model: {e}")
        return None

@st.cache_data
def find_database():
    """Find the database directory with extended search"""
    for path in POSSIBLE_DB_PATHS:
        if os.path.exists(path):
            st.success(f"✅ Database found at: {path}")
            return path
    
    # Additional debug information
    st.error("❌ Database not found in any expected location")
    with st.expander("🔍 Debug Information"):
        st.write("**Current working directory:**", os.getcwd())
        st.write("**Files in current directory:**")
        try:
            files = os.listdir(".")
            for file in files:
                st.write(f"- {file}")
        except Exception as e:
            st.write(f"Error listing files: {e}")
        
        st.write("**Searched paths:**")
        for path in POSSIBLE_DB_PATHS:
            exists = os.path.exists(path)
            st.write(f"- {path}: {'✅ Found' if exists else '❌ Not found'}")
    
    return None

@st.cache_resource
def connect_to_database():
    """Connect to ChromaDB and return collections with robust error handling"""
    if not CHROMADB_AVAILABLE:
        return None, {}
    
    db_path = find_database()
    if not db_path:
        return None, {}
    
    try:
        # Try different ChromaDB configurations for cloud compatibility
        settings = Settings(
            anonymized_telemetry=False,
            allow_reset=False,
            is_persistent=True
        )
        
        client = chromadb.PersistentClient(
            path=db_path,
            settings=settings
        )
        
        collections = client.list_collections()
        st.success(f"✅ Connected to ChromaDB with {len(collections)} collections")
        return db_path, {col.name: col for col in collections}
        
    except Exception as e:
        st.error(f"❌ Database connection error: {str(e)}")
        
        # Try alternative ChromaDB configuration
        try:
            st.info("🔄 Trying alternative ChromaDB configuration...")
            client = chromadb.PersistentClient(path=db_path)
            collections = client.list_collections()
            st.success(f"✅ Alternative connection successful with {len(collections)} collections")
            return db_path, {col.name: col for col in collections}
        except Exception as e2:
            st.error(f"❌ Alternative connection also failed: {str(e2)}")
            
            # Provide troubleshooting information
            with st.expander("🛠️ Troubleshooting Information"):
                st.write("**Original Error:**", str(e))
                st.write("**Alternative Error:**", str(e2))
                st.write("**Database Path:**", db_path)
                st.write("**Python Version:**", st.session_state.get('python_version', 'Unknown'))
                st.write("**ChromaDB Available:**", CHROMADB_AVAILABLE)
                
                # Check database files
                if os.path.exists(db_path):
                    try:
                        db_files = os.listdir(db_path)
                        st.write("**Database files found:**")
                        for file in db_files:
                            file_path = os.path.join(db_path, file)
                            size = os.path.getsize(file_path) if os.path.isfile(file_path) else "directory"
                            st.write(f"- {file}: {size}")
                    except Exception as e3:
                        st.write(f"Error reading database directory: {e3}")
            
            return None, {}

def display_header():
    """Display the main header and branding"""
    st.markdown('<h1 class="main-header">🍛 North Indian Cuisine Discovery</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Recipe & Ingredient Search System</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔍 **Semantic Search**")
        st.caption("Intelligent recipe discovery")
    with col2:
        st.markdown("🧠 **AI-Powered**")
        st.caption("Advanced NLP understanding")
    with col3:
        st.markdown("🍽️ **Authentic Recipes**")
        st.caption("Traditional North Indian cuisine")

def display_error_message():
    """Display comprehensive error message for deployment issues"""
    st.markdown("""
    <div class="error-container">
        <h3>🚨 System Error Detected</h3>
        <p>Your RAG system encountered a compatibility issue, likely related to ChromaDB on Streamlit Cloud.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔧 Common Solutions:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **For Streamlit Cloud:**
        1. Check requirements.txt versions
        2. Ensure packages.txt includes system dependencies  
        3. Verify Python version compatibility
        4. Check database file paths
        """)
    
    with col2:
        st.markdown("""
        **For Local Development:**
        1. Rebuild Docker image
        2. Clear browser cache
        3. Restart Streamlit server
        4. Check Docker logs for details
        """)
    
    with st.expander("🔍 Debug Information"):
        st.write("**Environment Details:**")
        st.write(f"- Current Directory: {os.getcwd()}")
        st.write(f"- ChromaDB Available: {CHROMADB_AVAILABLE}")
        st.write(f"- Sentence Transformers Available: {SENTENCE_TRANSFORMERS_AVAILABLE}")
        
        st.write("**Expected Files:**")
        expected_files = [
            "clean_north_indian_rag_data.json",
            "north_indian_rag_db/",
            "requirements.txt",
            "packages.txt"
        ]
        
        for file in expected_files:
            exists = os.path.exists(file)
            st.write(f"- {file}: {'✅' if exists else '❌'}")

def display_database_stats(db_path, collections):
    """Display database statistics in an attractive layout"""
    st.markdown("### 📊 Database Overview")
    
    if not collections:
        st.error("❌ No database collections found")
        display_error_message()
        return False
    
    # Create metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_docs = sum(col.count() for col in collections.values())
    
    with col1:
        st.metric(
            label="🗄️ Database Status",
            value="Connected",
            delta="✅ Active"
        )
    
    with col2:
        st.metric(
            label="📚 Total Documents",
            value=f"{total_docs:,}",
            delta=f"{len(collections)} collections"
        )
    
    with col3:
        recipes_count = collections.get('north_indian_recipes', type('', (), {'count': lambda: 0})).count()
        st.metric(
            label="🍛 Recipes",
            value=f"{recipes_count:,}",
            delta="North Indian dishes"
        )
    
    with col4:
        ingredients_count = collections.get('ingredient_usage', type('', (), {'count': lambda: 0})).count()
        st.metric(
            label="🥬 Ingredients",
            value=f"{ingredients_count:,}",
            delta="Ingredient profiles"
        )
    
    # Collection details in expandable section
    with st.expander("🔍 Collection Details", expanded=False):
        for name, collection in collections.items():
            col_icon = "🍛" if "recipe" in name else "🥬" if "ingredient" in name else "🔍"
            st.write(f"{col_icon} **{name.replace('_', ' ').title()}**: {collection.count():,} documents")
    
    return True

def create_search_interface(collections, model):
    """Create the main search interface"""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown("### 🔍 Discover North Indian Cuisine")
    
    # Search configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Collection selection with descriptions
        collection_options = {
            "north_indian_recipes": "🍛 Recipe Search - Find complete recipes and ingredient lists",
            "ingredient_usage": "🥬 Ingredient Search - Discover dishes using specific ingredients", 
            "general_food_search": "🔍 General Search - Explore cuisine types and cooking styles"
        }
        
        selected_collection = st.selectbox(
            "Choose Search Type:",
            options=list(collection_options.keys()),
            format_func=lambda x: collection_options[x],
            key="collection_select"
        )
    
    with col2:
        search_examples = {
            "north_indian_recipes": ["Dal Makhani", "Butter Chicken", "Chole Bhature"],
            "ingredient_usage": ["paneer", "ghee", "cardamom"],
            "general_food_search": ["Punjabi breakfast", "vegetarian dishes", "street food"]
        }
        
        st.markdown("**💡 Example Searches:**")
        for example in search_examples.get(selected_collection, []):
            if st.button(f"'{example}'", key=f"example_{example}", help=f"Search for {example}"):
                st.session_state.search_query = example
    
    # Search input
    query = st.text_input(
        "Enter your search query:",
        placeholder="e.g., What ingredients are in Dal Makhani?",
        value=st.session_state.get('search_query', ''),
        key="main_search"
    )
    
    # Advanced options
    with st.expander("⚙️ Advanced Search Options"):
        col1, col2 = st.columns(2)
        with col1:
            num_results = st.slider("Number of results:", 1, 20, 5)
        with col2:
            min_confidence = st.slider("Minimum confidence:", 0.0, 1.0, 0.3, 0.1)
    
    # Search button
    search_clicked = st.button("🔍 Search Recipes", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return selected_collection, query, num_results, min_confidence, search_clicked

def display_search_results(collection, query, model, num_results, min_confidence):
    """Display search results in an attractive format with robust error handling"""
    
    with st.spinner("🔍 Searching through thousands of authentic North Indian recipes..."):
        try:
            # Perform search
            start_time = time.time()
            results = collection.query(
                query_texts=[query],
                n_results=num_results,
                include=['documents', 'metadatas', 'distances']
            )
            search_time = time.time() - start_time
            
            if not results['documents'][0]:
                st.warning("No results found. Try a different search term or reduce the minimum confidence.")
                return
            
            # Filter by confidence
            filtered_results = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                confidence = 1 - distance
                if confidence >= min_confidence:
                    filtered_results.append((doc, metadata, confidence, i))
            
            if not filtered_results:
                st.warning(f"No results found with confidence ≥ {min_confidence:.1%}. Try lowering the minimum confidence.")
                return
            
            # Display results header
            st.markdown(f"### 🎯 Search Results for '{query}'")
            st.caption(f"Found {len(filtered_results)} results in {search_time:.2f} seconds")
            
            # Display individual results
            for i, (doc, metadata, confidence, orig_idx) in enumerate(filtered_results):
                
                # Determine confidence level for styling
                if confidence >= 0.8:
                    confidence_class = "confidence-high"
                    confidence_emoji = "🟢"
                elif confidence >= 0.6:
                    confidence_class = "confidence-medium"
                    confidence_emoji = "🟡"
                else:
                    confidence_class = "confidence-low"
                    confidence_emoji = "🔴"
                
                # Create result card
                with st.container():
                    st.markdown(f"""
                    <div class="result-card {confidence_class}">
                        <h4>{confidence_emoji} Result {i+1} - {confidence:.1%} Confidence</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Main content
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("**📝 Content:**")
                        # Truncate long content
                        display_content = doc[:400] + "..." if len(doc) > 400 else doc
                        st.write(display_content)
                    
                    with col2:
                        st.markdown("**ℹ️ Details:**")
                        if 'recipe_name' in metadata:
                            st.write(f"🍽️ **Recipe:** {metadata['recipe_name']}")
                        if 'cuisine' in metadata:
                            st.write(f"🌍 **Cuisine:** {metadata['cuisine']}")
                        if 'course' in metadata:
                            st.write(f"🍴 **Course:** {metadata['course']}")
                        if 'ingredient_name' in metadata:
                            st.write(f"🥬 **Ingredient:** {metadata['ingredient_name']}")
                    
                    # Additional metadata in expandable section
                    with st.expander(f"🔍 View Full Details - Result {i+1}"):
                        st.json(metadata)
                        st.markdown("**Full Content:**")
                        st.text(doc)
                    
                    st.markdown("---")
        
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            st.info("Please try a different search term or check your database connection.")
            
            with st.expander("🔍 Error Details"):
                st.write(f"**Error Type:** {type(e).__name__}")
                st.write(f"**Error Message:** {str(e)}")
                st.write(f"**Query:** {query}")
                st.write(f"**Collection:** {collection.name if hasattr(collection, 'name') else 'Unknown'}")

def create_sidebar():
    """Create an informative sidebar with system status"""
    with st.sidebar:
        st.markdown("# 🍛 Navigation")
        
        # System status
        st.markdown("## 📊 System Status")
        db_path, collections = connect_to_database()
        
        if collections:
            st.success("✅ Database Connected")
            total_docs = sum(col.count() for col in collections.values())
            st.metric("Total Documents", f"{total_docs:,}")
        else:
            st.error("❌ Database Offline")
            st.info("Check deployment configuration")
        
        # Model status
        model = load_embedding_model()
        if model:
            st.success("✅ AI Model Loaded")
        else:
            st.error("❌ AI Model Failed")
        
        st.markdown("---")
        
        # Search tips
        st.markdown("## 💡 Search Tips")
        st.markdown("""
        **Recipe Search:**
        - "Dal Makhani ingredients"
        - "Butter chicken recipe"
        - "Chole Bhature components"
        
        **Ingredient Search:**
        - "dishes with paneer"
        - "recipes using ghee"
        - "cardamom usage"
        
        **General Search:**
        - "Punjabi breakfast dishes"
        - "vegetarian North Indian"
        - "traditional street food"
        """)
        
        st.markdown("---")
        
        # About section
        st.markdown("## ℹ️ About")
        st.markdown("""
        This AI-powered system helps you discover authentic North Indian cuisine through intelligent search across thousands of traditional recipes.
        
        **Features:**
        - 🧠 Semantic search understanding
        - 🍛 3,500+ authentic recipes
        - 🥬 Detailed ingredient analysis
        - 🔍 Multi-type search capabilities
        """)
        
        st.markdown("---")
        st.caption("🔧 Built with Streamlit & ChromaDB")

def main():
    """Main application function with comprehensive error handling"""
    # Initialize session state
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    
    # Store Python version for debugging
    import sys
    st.session_state.python_version = sys.version
    
    # Create sidebar
    create_sidebar()
    
    # Display header
    display_header()
    
    # Check system requirements
    if not CHROMADB_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
        display_error_message()
        return
    
    # Connect to database
    db_path, collections = connect_to_database()
    
    if not db_path or not collections:
        st.error("❌ Vector database connection failed!")
        display_error_message()
        return
    
    # Display database stats
    if not display_database_stats(db_path, collections):
        return
    
    # Load embedding model
    model = load_embedding_model()
    if not model:
        st.error("❌ Failed to load AI model!")
        display_error_message()
        return
    
    st.success("✅ AI model loaded and ready")
    
    st.markdown("---")
    
    # Search interface
    selected_collection, query, num_results, min_confidence, search_clicked = create_search_interface(collections, model)
    
    # Perform search
    if search_clicked and query:
        if selected_collection in collections:
            display_search_results(
                collections[selected_collection], 
                query, 
                model, 
                num_results, 
                min_confidence
            )
        else:
            st.error(f"Collection '{selected_collection}' not found in database.")
    elif search_clicked:
        st.warning("Please enter a search query.")

if __name__ == "__main__":
    main()
