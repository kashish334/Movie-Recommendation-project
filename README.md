# Movie-Recommendation-project

This project is a movie recommendation system built using PySpark’s ALS collaborative filtering algorithm for user–movie rating predictions and a content-based cosine similarity model over movie genres for “similar movies” search, exposed through a Streamlit web app.

This project is built with Streamlit and deployed on Streamlit Community Cloud.

## Features
- **Collaborative Filtering**
  - Uses Spark MLlib’s ALS algorithm
  - Predicts top-N movies for each user
- **Content-Based Filtering**
  - Finds movies similar to a given title using genre vectors
- **Scalable**
  - Built on PySpark for handling large datasets
- **Interactive UI**
  - Streamlit app for easy interaction
 
## Project Structure
- `inference.py` - Movie similarity logic (cosine similarity)
- `movie_app.py` - Streamlit application
- `Training_ALS_model.py` - Trains ALS model & generates recommendations
- artifacts
    - `movies_rec_user.csv` - Generated recommendations (training output)
- `requirements.txt`

## ⚙️ Tech Stack

- **Python**
- **PySpark**
- **Spark MLlib (ALS)**
- **Pandas**
- **Streamlit**

## 🧠 Recommendation Approaches

### 1️⃣ Collaborative Filtering (ALS)
- Learns latent user–movie interactions
- Generates top-5 movie recommendations per user
- Output saved as: `artifacts/movies_rec_user.csv`

### 2️⃣ Content-Based Filtering
- Uses movie genres
- Computes cosine similarity between movies
- Finds similar movies for a given title

## ▶️ How to Run the Project
