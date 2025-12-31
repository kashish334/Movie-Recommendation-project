FROM python:3.9-slim-bullseye

# Install Java (Required for PySpark)
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    && apt-get clean

WORKDIR /app

# Copy all files. Because of Step 1, these will be the REAL 100MB+ files, 
# not the tiny pointer files.
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Render expects port 10000
EXPOSE 10000

CMD ["streamlit", "run", "movie_app.py", "--server.port=10000", "--server.address=0.0.0.0"]