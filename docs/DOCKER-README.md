# 🐳 Quick Start with Docker

## Option 1: Super Easy (Windows)
```bash
# Just double-click this file:
run-local.bat
```

## Option 2: Super Easy (Linux/Mac)
```bash
# Make script executable and run:
chmod +x run-local.sh
./run-local.sh
```

## Option 3: Docker Commands
```bash
# Build and run manually:
docker build -t north-indian-rag .
docker run -p 8501:8501 north-indian-rag
```

## Option 4: Docker Compose
```bash
# Even easier management:
docker-compose up
# Stop with: docker-compose down
```

## 🌐 Access Your App
Once running, open: **http://localhost:8501**

## 🧪 Test Your RAG System
Try searching for:
- "What's in Dal Makhani?"
- "dishes with paneer"
- "North Indian breakfast"

## 🛑 Stop the App
- **Scripts**: Press Ctrl+C
- **Docker**: `docker stop <container-id>`
- **Compose**: `docker-compose down`

## 📊 Expected Performance
- **Build time**: 3-5 minutes (first time)
- **Start time**: 30-60 seconds
- **Memory usage**: ~1-2GB
- **Search speed**: <2 seconds per query

## ✅ Success Indicators
- ✅ "You can now view your Streamlit app in your browser"
- ✅ Green "Database Connected" in sidebar
- ✅ Search returns ingredient lists
- ✅ No error messages in logs

## 🐛 Troubleshooting
- **Port busy**: Kill process on 8501 or use different port
- **Build fails**: Run `docker system prune -f` and rebuild
- **App won't start**: Check `docker logs <container-id>`

Ready to test your RAG system! 🚀
