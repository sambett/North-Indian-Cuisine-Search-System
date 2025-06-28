# Basic Dockerfile for North Indian RAG (no allergen detection)
FROM python:3.10-slim

WORKDIR /app

# Copy only essential files
COPY requirements.txt .
COPY streamlit_rag_app_fixed.py .
COPY build_vector_database.py .
COPY clean_north_indian_rag_data.json .

# Copy the vector database
COPY north_indian_rag_db/ ./north_indian_rag_db/

# Install dependencies (skip allergen requirements)
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the original streamlit app
CMD ["streamlit", "run", "streamlit_rag_app_fixed.py", "--server.port=8501", "--server.address=0.0.0.0"]
