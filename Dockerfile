FROM python:3.9-slim

WORKDIR /app

# Install only what's needed for FAISS + Streamlit (no Spark/Java!)
RUN apt-get update && apt-get install -y \
    libopenblas-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt faiss-cpu pandas==2.0.3 numpy streamlit

COPY . . 

# Preload data/metadata (faster startup)
RUN python -c "import pandas as pd; df=pd.read_csv('data/movies.csv'); print(f'✅ Loaded {len(df)} movies')"

EXPOSE 8501

CMD ["streamlit", "run", "movie_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
