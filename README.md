# 🍛 North Indian Cuisine Semantic Search

A CPU-optimized semantic search system for North Indian recipes using vector embeddings and ChromaDB.

## ✨ What This System Does

- **Semantic Recipe Search**: Find recipes by ingredients, dish names, or cooking styles using AI embeddings
- **Fast Performance**: Sub-second search responses across 3,499+ North Indian recipes  
- **Multi-Search Types**: Recipe-to-ingredients, ingredient-to-recipes, and general food queries
- **CPU-Only Deployment**: No GPU requirements, runs efficiently on standard hardware

## 🚀 Quick Start

### Docker (Recommended)
```bash
docker build -t north-indian-rag .
docker run -p 8501:8501 north-indian-rag
# Open: http://localhost:8501
```

### Local Development
```bash
pip install -r requirements.txt
streamlit run streamlit_rag_app_fixed.py
```

## 🎥 System Demo

**Watch the RAG system in action:** [https://youtu.be/oGl7WEDB8m8](https://youtu.be/oGl7WEDB8m8)

> **Note**: This demo shows an earlier version with local LLM integration (Ollama). The current production version uses CPU-only semantic search without LLM generation for improved performance and reduced resource requirements. The core search functionality and database remain the same.

## 📊 System Performance (Real Data)

Based on actual testing with live database:

- **Database Size**: 3,499 North Indian recipes + 1,000 ingredient documents
- **Average Response Time**: 0.416 seconds
- **Search Success Rate**: 100% (all queries return results)
- **Memory Usage**: ~1GB RAM for full operation
- **Storage**: 60MB vector database + 36MB recipe data

**Sample Search Results**:
- "Dal Makhani" → 0.607s response, finds lentil recipes
- "paneer dishes" → 0.329s response, 41.4% confidence match
- "North Indian food" → 0.478s response, 38.3% confidence match

## 🏗️ Architecture

### Data Pipeline
1. **Raw Data**: Kaggle Indian Food Dataset (6,871 recipes)
2. **Processing**: `clean_process_indian_food.py` filters to 3,499 North Indian recipes
3. **Vectorization**: `build_vector_database.py` creates embeddings using Sentence Transformers
4. **Storage**: ChromaDB with 3 specialized collections

### Search System
- **Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional vectors)
- **Vector Database**: ChromaDB with persistent storage
- **Search Types**: 
  - Recipe search (find ingredients in dishes)
  - Ingredient search (find dishes using specific ingredients)
  - General food queries (broad cuisine exploration)

### Architecture Evolution
- **Previous Version** (shown in demo): Local LLM with Ollama for natural language generation
- **Current Version**: CPU-optimized semantic search without LLM for better performance and deployment simplicity

## 📁 Key Files

- `streamlit_rag_app_fixed.py` - Web interface
- `build_vector_database.py` - Vector database creation
- `clean_process_indian_food.py` - Data processing pipeline
- `clean_north_indian_rag_data.json` - Processed recipe database (36MB)
- `north_indian_rag_db/` - ChromaDB vector database (25MB)

## 🛠️ Technology Stack

- **Python 3.10+**
- **Streamlit** - Web interface
- **ChromaDB** - Vector database
- **Sentence Transformers** - Text embeddings
- **Docker** - Containerized deployment

## 📈 Search Capabilities

### What Works Well
- Finding recipes by dish name (e.g., "Dal Makhani" finds lentil recipes)
- Ingredient-based search (e.g., "paneer dishes" returns cottage cheese recipes)
- Regional cuisine queries (e.g., "North Indian food" returns appropriate results)
- Fast response times under 1 second

### Current Limitations
- Confidence scores average 31.4% (functional but could be improved)
- Limited semantic understanding for some ingredient synonyms
- English-only interface (no Hindi translation currently active)

## 🔧 Setup Requirements

```bash
# Install dependencies
pip install streamlit>=1.28.0 chromadb==1.0.13 sentence-transformers==4.1.0 pandas numpy torch

# Build vector database (one-time setup)
python build_vector_database.py

# Run application
streamlit run streamlit_rag_app_fixed.py
```

## 🐳 Docker Deployment

The system includes production-ready Docker configuration:

```dockerfile
FROM python:3.10-slim
# Includes all dependencies and data
# Final image: ~2GB (includes AI models and vector database)
```

**No rebuild required** for README updates - Docker image contains the full system.

## 🧪 Testing

Verify your setup:
```bash
python scripts/check_collections.py  # Check database collections
```

Expected output:
- `north_indian_recipes`: 3,499 documents
- `ingredient_usage`: 1,000 documents  
- `general_food_search`: 100 documents

## 🎯 Use Cases

- **Recipe Discovery**: "What ingredients are in Chole Bhature?"
- **Ingredient Exploration**: "Which dishes use paneer?"
- **Cuisine Research**: "Traditional North Indian breakfast dishes"
- **Cooking Planning**: Find recipes based on available ingredients

## 🔮 Future Work

Future enhancements include LLM-based response generation and improved evaluation scoring, but these are currently not integrated due to compute constraints (CPU-only setup).

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built for efficient semantic search of North Indian cuisine without GPU requirements.**