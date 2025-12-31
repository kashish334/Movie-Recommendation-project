# 1. Start with a Python base image
FROM python:3.9-slim-bullseye

# 2. Install OpenJDK (Java) and other system dependencies
# PySpark needs Java to run.
RUN apt-get update --fix-missing && apt-get install -y \
    openjdk-11-jre-headless \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Set Environment Variables
# This is the Docker equivalent of your manual 'Path' settings
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# 4. Set the working directory inside the container
WORKDIR /app

# 5. Copy your requirements file and install Python libraries
# (Ensure pyspark and streamlit are in your requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your project files (dataset, app.py, etc.)
COPY . .

# 7. Expose the port Streamlit uses
EXPOSE 8501

# 8. Start the app
CMD ["streamlit", "run", "movie_app.py", "--server.port=8501", "--server.address=0.0.0.0"]