FROM python:3.9-slim-bullseye

# 1. Install Java, Git, and Git-LFS
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    git \
    git-lfs \
    && git lfs install \
    && apt-get clean

WORKDIR /app

# 2. Copy all files (at this point, LFS files are just tiny text pointers)
COPY . /app

# 3. FORCE the download of the real 100MB+ files
# Note: This requires the repo to be a valid git repo or handled via smudge
# If this fails, we use the 'Skip Smudge' env var approach below.
RUN git lfs pull

RUN pip install --no-cache-dir -r requirements.txt

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
EXPOSE 10000

CMD ["streamlit", "run", "movie_app.py", "--server.port=10000", "--server.address=0.0.0.0"]