@echo off
REM Quick Docker setup script for North Indian RAG

echo 🐳 North Indian RAG - Docker Local Setup
echo =========================================

REM Check if Docker is running
echo 📋 Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not found! Please install Docker Desktop first.
    echo Download from: https://docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker found!

REM Check if we're in the right directory
if not exist "streamlit_rag_app_fixed.py" (
    echo ❌ streamlit_rag_app_fixed.py not found!
    echo Please run this script from the northindian_rag directory
    pause
    exit /b 1
)

echo ✅ Project files found!

REM Build Docker image
echo.
echo 🔧 Building Docker image (this may take 3-5 minutes)...
docker build -t north-indian-rag .

if errorlevel 1 (
    echo ❌ Docker build failed! Check the error messages above.
    pause
    exit /b 1
)

echo ✅ Docker image built successfully!

REM Check if port 8501 is already in use
netstat -an | find "8501" | find "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Port 8501 is already in use. Trying to kill existing process...
    for /f "tokens=5" %%a in ('netstat -ano ^| find "8501" ^| find "LISTENING"') do taskkill /PID %%a /F >nul 2>&1
    timeout /t 2 >nul
)

REM Run the container
echo.
echo 🚀 Starting North Indian RAG application...
echo.
echo 📖 Instructions:
echo    1. Wait for "You can now view your Streamlit app in your browser"
echo    2. Open: http://localhost:8501
echo    3. Test search: "What's in Dal Makhani?"
echo    4. Press Ctrl+C to stop the application
echo.

docker run -p 8501:8501 --name rag-app-local north-indian-rag

REM Cleanup after stopping
echo.
echo 🧹 Cleaning up...
docker stop rag-app-local >nul 2>&1
docker rm rag-app-local >nul 2>&1

echo.
echo 👋 Application stopped. Thanks for using North Indian RAG!
pause
