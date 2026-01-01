FROM python:3.9-slim-bullseye

# 1. Install Java, Git, and Git-LFS
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    git \
    git-lfs \
    && git lfs install \
    && apt-get clean

WORKDIR /app

# Clone repo with LFS skip (respects GIT_LFS_SKIP_SMUDGE=1 env var)
ARG REPO_URL=https://github.com/kashish334/Movie-Recommendation-project.git
ARG REPO_BRANCH=main  # or your branch
RUN git clone --depth 1 --branch ${REPO_BRANCH} --single-branch ${REPO_URL} . \
    && git lfs pull  # Downloads real LFS files here

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
EXPOSE 10000

CMD ["streamlit", "run", "movie_app.py", "--server.port=10000", "--server.address=0.0.0.0"]