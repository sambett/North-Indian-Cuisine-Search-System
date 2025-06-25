# Use a lightweight official Python base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy all your files into the container INCLUDING the database
COPY . .

# Install required Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make sure the database directory exists and is accessible
RUN ls -la north_indian_rag_db/

# Expose Streamlit's default port
EXPOSE 8501

# Set the correct working directory
WORKDIR /app

# Run the FIXED Streamlit app
CMD ["streamlit", "run", "streamlit_rag_app_fixed.py"]
