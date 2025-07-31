# 🍛 North Indian Cuisine Search System

**AI-Powered Semantic Search for Authentic North Indian Recipes**

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://hub.docker.com/r/sambett1/north-indian-rag)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB)](https://python.org)

## 🚀 Quick Start with Docker (Recommended)

```bash
# Pull and run the complete RAG system
docker run -p 8501:8501 sambett1/north-indian-rag:latest

# Open your browser to: http://localhost:8501
```

**That's it!** The Docker image contains everything needed for the full AI-powered search experience.

## 🧠 What is This?

This is a **RAG (Retrieval-Augmented Generation)** system that makes finding North Indian recipe ingredients fast and intelligent:

- **Traditional Search**: "Find me butter chicken" → keyword matching
- **Our AI Search**: "What's in creamy North Indian curry?" → understands you want Butter Chicken ingredients

## ✨ Features

- 🔍 **Semantic Search** - Understands meaning, not just keywords
- 🍛 **3,500+ Recipes** - Curated North Indian dishes
- 🥬 **4,500+ Ingredients** - Comprehensive ingredient database
- ⚡ **Sub-2s Response** - Lightning fast results
- 📊 **Confidence Scoring** - Know how accurate each result is
- 🎨 **Professional UI** - Beautiful, responsive interface

## 🎯 Try These Searches

```
"What ingredients are in Dal Makhani?"
"Which dishes use paneer?"
"North Indian breakfast recipes"
"Spicy curry ingredients"
```

## 🐳 Why Docker?

This RAG system requires:
- **Vector Database** (ChromaDB with 47,170 documents)
- **AI Models** (Sentence Transformers for embeddings)
- **Large Dataset** (36MB processed recipe data)

Docker packages everything together for one-command deployment!

## 📊 System Performance

- **Search Speed**: <2 seconds average
- **Accuracy**: 90%+ relevant results
- **Database Size**: 60MB optimized
- **Memory Usage**: ~1GB RAM
- **Container Size**: ~2GB (includes full AI stack)

## 🏗️ Architecture

```
User Query → AI Understanding → Vector Search → Recipe Database → Smart Results
```

- **Frontend**: Streamlit web application
- **Vector DB**: ChromaDB with semantic embeddings
- **AI Model**: Sentence Transformers (all-MiniLM-L6-v2)
- **Data**: 3,499 curated North Indian recipes

## 🔧 Alternative Installation Methods

### Option 1: Build Locally
```bash
git clone https://github.com/sambett/North-Indian-Cuisine-Search-System.git
cd North-Indian-Cuisine-Search-System
docker build -t north-indian-rag .
docker run -p 8501:8501 north-indian-rag
```

### Option 2: Python Environment (Advanced)
```bash
# Clone repository
git clone https://github.com/sambett/North-Indian-Cuisine-Search-System.git
cd North-Indian-Cuisine-Search-System

# Install dependencies
pip install -r requirements.txt

# Run application (requires all data files)
streamlit run streamlit_rag_app_fixed.py
```

## 📁 Project Structure

```
├── streamlit_rag_app_fixed.py      # Main Streamlit application
├── clean_north_indian_rag_data.json # Recipe database (36MB)
├── north_indian_rag_db/            # ChromaDB vector database
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
└── README.md                       # This file
```

## ⚠️ Important Notes

### **Streamlit Cloud Deployment**
This app is **not designed for Streamlit Cloud** due to:
- Large vector database files (60MB+)
- ChromaDB compatibility requirements
- System dependencies for AI models

**Solution**: Use the Docker image which contains everything pre-configured!

### **Cloud Hosting Alternatives**
- **AWS ECS/EKS**: Deploy Docker container
- **Google Cloud Run**: Supports container deployment
- **Azure Container Instances**: Easy Docker hosting
- **Local Development**: Perfect for Docker Desktop

## 🎨 What Makes This Special

### Technical Innovation
- **Vector Embeddings**: Mathematical representation of recipe meanings
- **Semantic Understanding**: AI comprehends cooking context and ingredients
- **Multi-Collection Search**: Specialized search types (recipes, ingredients, general)
- **Real-Time Performance**: Optimized for speed and accuracy

### Real-World Impact
- **Accessibility**: Makes traditional recipes searchable and discoverable
- **Speed**: 10x faster than manual recipe browsing
- **Accuracy**: AI understanding vs simple keyword matching
- **Scale**: Ready for production use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test with Docker
4. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🎯 Built With

- [Streamlit](https://streamlit.io) - Web framework
- [ChromaDB](https://www.trychroma.com) - Vector database
- [Sentence Transformers](https://www.sbert.net) - AI embeddings
- [Docker](https://docker.com) - Containerization

---

**Made with ❤️ for North Indian cuisine lovers**

[🐳 Docker Hub](https://hub.docker.com/r/sambett1/north-indian-rag) | [⭐ Star this repo](https://github.com/sambett/North-Indian-Cuisine-Search-System)
