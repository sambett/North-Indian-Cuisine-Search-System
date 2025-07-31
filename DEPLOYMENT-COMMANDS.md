# 🚀 Deployment Commands for North Indian RAG System

## Step 1: Push to GitHub

```powershell
# Navigate to your project directory
cd C:\Users\SelmaB\Desktop\northindian_rag

# Remove any existing remote
git remote remove origin

# Add your GitHub repository
git remote add origin https://github.com/sambett/North-Indian-Cuisine-Search-System.git

# Stage all files
git add .

# Commit with professional message
git commit -m "feat: Complete North Indian RAG system with AI evaluation

- Semantic search with vector embeddings (47K documents)
- Hindi recipe translation system  
- Professional evaluation metrics and analytics
- Sub-2-second response time with 90%+ accuracy
- Production-ready Docker containerization
- Professional Streamlit interface with confidence scoring

Tech Stack: ChromaDB, Sentence Transformers, Streamlit, Docker
Data: 3,499 curated North Indian recipes, 4,459 unique ingredients"

# Push to GitHub (force push to overwrite existing)
git branch -M main
git push -u origin main --force
```

## Step 2: Push Docker Image to Docker Hub

```powershell
# Login to Docker Hub (enter username: sambett1 and your password)
docker login

# Tag your image for Docker Hub
docker tag north-indian-rag sambett1/north-indian-rag:latest
docker tag north-indian-rag sambett1/north-indian-rag:v1.0

# Push to Docker Hub (this uploads ~2GB)
docker push sambett1/north-indian-rag:latest
docker push sambett1/north-indian-rag:v1.0
```

## Step 3: Verify Deployment

### Check GitHub
Visit: https://github.com/sambett/North-Indian-Cuisine-Search-System

### Check Docker Hub  
Visit: https://hub.docker.com/r/sambett1/north-indian-rag

### Test Public Access
```powershell
# Anyone can now run your app with:
docker run -p 8501:8501 sambett1/north-indian-rag:latest
```

## Expected Timeline

- **GitHub Push**: 1-2 minutes (65MB upload)
- **Docker Login**: 30 seconds  
- **Docker Push**: 15-30 minutes (2GB upload)
- **Total**: ~35 minutes

## Troubleshooting

### Git Issues
```powershell
# If git push fails, check credentials:
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# If repository doesn't exist, create it on GitHub first
```

### Docker Issues
```powershell
# If Docker login fails:
docker logout
docker login

# Check image exists before pushing:
docker images | findstr north-indian-rag
```

### Network Issues
```powershell
# Large upload - ensure stable internet
# If push fails, retry:
docker push sambett1/north-indian-rag:latest
```

## Success Indicators

✅ **GitHub**: Repository updated with all files  
✅ **Docker Hub**: Image available at sambett1/north-indian-rag  
✅ **Public Access**: Anyone can run with docker run command  
✅ **Documentation**: Professional README displayed  

## Image Details

- **Repository**: sambett1/north-indian-rag
- **Tags**: latest, v1.0
- **Size**: ~2GB (includes full AI stack)
- **Architecture**: linux/amd64
- **Base**: python:3.10-slim

## Public Usage

Once deployed, anyone can use your RAG system:

```bash
# Pull and run
docker pull sambett1/north-indian-rag:latest
docker run -p 8501:8501 sambett1/north-indian-rag:latest

# Open browser to: http://localhost:8501
```

Your AI-powered North Indian cuisine search system will be publicly available! 🌟
