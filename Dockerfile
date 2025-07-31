# Dockerfile for North Indian RAG - Production Ready
FROM python:3.10-slim

WORKDIR /app

# Copy only the files that exist and are needed
COPY requirements.txt .
COPY streamlit_rag_app_fixed.py .
COPY clean_north_indian_rag_data.json .

# Copy the vector database directory
COPY north_indian_rag_db/ ./north_indian_rag_db/

# Copy Streamlit config
COPY .streamlit/ ./.streamlit/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_rag_app_fixed.py", "--server.port=8501", "--server.address=0.0.0.0"]
