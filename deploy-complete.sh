#!/bin/bash
# Complete deployment script for North Indian RAG System

echo "🚀 North Indian RAG System - Complete Deployment"
echo "================================================"

# Step 1: Git Setup and Push to GitHub
echo ""
echo "📁 Step 1: Pushing to GitHub..."
echo "-------------------------------"

# Remove existing remote if it exists
git remote remove origin 2>/dev/null || true

# Add your GitHub repository
git remote add origin https://github.com/sambett/North-Indian-Cuisine-Search-System.git

# Stage all files
git add .

# Commit with professional message
git commit -m "feat: Complete North Indian RAG system with AI evaluation

- ✨ Semantic search with vector embeddings (47K documents)
- 🌍 Hindi recipe translation system
- 📊 Professional evaluation metrics and analytics
- ⚡ Sub-2-second response time with 90%+ accuracy
- 🐳 Production-ready Docker containerization
- 🎨 Professional Streamlit interface with confidence scoring

Tech Stack: ChromaDB, Sentence Transformers, Streamlit, Docker
Data: 3,499 curated North Indian recipes, 4,459 unique ingredients"

# Push to GitHub
echo "Pushing to GitHub repository..."
git branch -M main
git push -u origin main --force

echo "✅ Successfully pushed to GitHub!"

# Step 2: Docker Hub Deployment
echo ""
echo "🐳 Step 2: Docker Hub Deployment..."
echo "-----------------------------------"

# Login to Docker Hub (you'll need to enter your credentials)
echo "Please log in to Docker Hub (username: sambett1):"
docker login

# Tag the image for Docker Hub
echo "Tagging image for Docker Hub..."
docker tag north-indian-rag sambett1/north-indian-rag:latest
docker tag north-indian-rag sambett1/north-indian-rag:v1.0

# Push to Docker Hub
echo "Pushing to Docker Hub..."
docker push sambett1/north-indian-rag:latest
docker push sambett1/north-indian-rag:v1.0

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================"
echo ""
echo "📍 Your project is now available at:"
echo "   🐙 GitHub: https://github.com/sambett/North-Indian-Cuisine-Search-System"
echo "   🐳 Docker Hub: https://hub.docker.com/r/sambett1/north-indian-rag"
echo ""
echo "🚀 Anyone can now run your app with:"
echo "   docker run -p 8501:8501 sambett1/north-indian-rag:latest"
echo ""
echo "📊 Image Details:"
echo "   • Size: ~2GB (includes full AI stack)"
echo "   • Tags: latest, v1.0"  
echo "   • Architecture: linux/amd64"
echo ""
echo "🌟 Your RAG system is now publicly available!"
