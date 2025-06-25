# 🍛 North Indian Cuisine Search System

## AI-Powered Semantic Search for North Indian Recipes & Ingredients

A sophisticated RAG (Retrieval-Augmented Generation) system that enables intelligent search across thousands of authentic North Indian recipes using vector embeddings and semantic similarity.

![North Indian Cuisine Search System](https://img.shields.io/badge/AI-Powered-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen) ![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red) ![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-purple)

## 🌟 Features

- **🔍 Semantic Search**: Find recipes by ingredients, dish names, or cooking methods
- **🧠 AI-Powered**: Uses sentence transformers for intelligent query understanding  
- **📊 Vector Database**: ChromaDB with 50,000+ searchable recipe documents
- **🎯 Multi-Search Types**: Recipe search, ingredient search, and general food queries
- **🐳 Docker Ready**: Containerized for easy deployment and consistency
- **🎨 Beautiful UI**: Modern Streamlit interface with real-time results
- **📈 Confidence Scoring**: Shows relevance scores for search results

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Raw Data      │───▶│  Data Processing │───▶│  Vector Database│
│  (Kaggle CSV)   │    │     Pipeline     │    │   (ChromaDB)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │◀───│  Search Engine   │◀───│  AI Embeddings  │
│   Web App       │    │                  │    │ (Transformers)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start with Docker

### Prerequisites
- Docker installed on your system
- 8GB+ RAM recommended for optimal performance

### 1. Clone the Repository
```bash
git clone https://github.com/sambett/North-Indian-Cuisine-Search-System.git
cd North-Indian-Cuisine-Search-System
```

### 2. Get the Data
Since the vector database is too large for GitHub, you need to build it locally:

```bash
# Download the Kaggle Indian Food Dataset and place it in:
# data/raw/IndianFoodDatasetCSV.csv
```

### 3. Build the Vector Database
```bash
# Process the data and build the vector database
python clean_process_indian_food.py
python build_vector_database.py
```

### 4. Build and Run with Docker
```bash
# Build the Docker image
docker build -t northindianrag .

# Run the container
docker run -p 8501:8501 northindianrag
```

### 5. Access the Application
Open your browser and navigate to: **http://localhost:8501**

## 🛠️ Manual Setup (Alternative)

### Requirements
- Python 3.9+
- pip or conda

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the data processing pipeline
python clean_process_indian_food.py
python build_vector_database.py

# Launch the Streamlit app
streamlit run streamlit_rag_app_fixed.py
```

## 📊 Database Statistics

Once built, your system will contain:
- **3,499** North Indian recipes
- **43,671** ingredient usage documents  
- **3,499** general search documents
- **50,000+** total searchable documents

## 🔍 Search Capabilities

### Recipe Search
Find ingredients and details for specific dishes:
- *"What ingredients are in Dal Makhani?"*
- *"Show me Chole Bhature recipe details"*
- *"Find butter chicken ingredients"*

### Ingredient Search  
Discover dishes that use specific ingredients:
- *"Which dishes use paneer?"*
- *"Recipes with black lentils"*
- *"Dishes using garam masala"*

### General Search
Explore by cuisine type, region, or cooking style:
- *"Popular Punjabi dishes"*
- *"Vegetarian North Indian food"*
- *"Traditional Delhi cuisine"*

## 🎯 Geographic Coverage

Focuses on authentic recipes from:
- **Punjab** - Traditional Punjabi cuisine
- **Chandigarh** - Modern North Indian dishes  
- **Haryana** - Regional specialties
- **Delhi** - Street food and restaurant dishes

## 🧬 Technical Stack

- **Backend**: Python 3.9+
- **Vector Database**: ChromaDB 0.4.15
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Web Framework**: Streamlit
- **Containerization**: Docker
- **Data Processing**: Pandas, NumPy
- **Search**: Semantic similarity with cosine distance

## 📁 Project Structure

```
North-Indian-Cuisine-Search-System/
├── 📄 README.md                     # This file
├── 📄 Dockerfile                    # Docker configuration
├── 📄 requirements.txt              # Python dependencies
├── 📄 .gitignore                    # Git ignore rules
├── 📄 streamlit_rag_app_fixed.py    # Main Streamlit application
├── 📄 clean_process_indian_food.py  # Data cleaning pipeline
├── 📄 build_vector_database.py      # Vector database builder
├── 📄 check_collections.py          # Database verification tool
├── 📁 data/                         # Data directory (not in repo)
│   ├── raw/                         # Raw datasets
│   └── processed/                   # Cleaned data
└── 📁 north_indian_rag_db/          # Vector database (not in repo)
```

## 🔧 Configuration

### Environment Variables
- `ANONYMIZED_TELEMETRY=False` - Disables ChromaDB telemetry
- `CHROMA_TELEMETRY=False` - Additional telemetry control

### Performance Tuning
- **Batch Size**: Adjust in `build_vector_database.py` (default: 50)
- **Memory**: Increase Docker memory allocation for large datasets
- **CPU**: More cores = faster embedding generation

## 🐛 Troubleshooting

### Common Issues

**Database not found error:**
```bash
# Verify database exists
python check_collections.py
```

**Slow initial loading:**
- First run downloads AI models (~90MB)
- Subsequent runs are faster due to caching

**Docker volume mounting issues:**
```bash
# Use absolute paths for volume mounting
docker run -p 8501:8501 -v "/full/path/to/project:/app" northindianrag
```

### Performance Tips
- Allow 1-3 minutes for initial model loading
- Search queries take 5-15 seconds (normal for semantic search)
- Use SSD storage for better I/O performance

## 📈 Future Enhancements

- [ ] **GPU Acceleration** for faster embeddings
- [ ] **Recipe Recommendations** based on user preferences  
- [ ] **Nutritional Information** integration
- [ ] **Multi-language Support** (Hindi, Punjabi)
- [ ] **Voice Search** capabilities
- [ ] **Recipe Image Recognition**
- [ ] **Meal Planning** features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature"`
5. Push to your fork: `git push origin feature-name`
6. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Data Source**: Kaggle Indian Food Dataset by Archana's Kitchen
- **AI Models**: Sentence Transformers by Hugging Face
- **Vector Database**: ChromaDB by the Chroma team
- **Web Framework**: Streamlit by Snowflake

## 📧 Contact

**Project Maintainer**: [sambett](https://github.com/sambett)

**Issues**: Please report bugs and feature requests via [GitHub Issues](https://github.com/sambett/North-Indian-Cuisine-Search-System/issues)

---

## 🌟 Star this Repository

If you found this project helpful, please consider giving it a ⭐ star on GitHub!

---

*Built with ❤️ for North Indian cuisine enthusiasts and AI developers*
