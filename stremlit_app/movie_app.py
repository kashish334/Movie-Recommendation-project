import streamlit as st
import pandas as pd
import requests

DATABRICKS_URL = st.secrets["DATABRICKS_URL"]
TOKEN = st.secrets["TOKEN"]

@st.cache_data
def load_data():
    recs = pd.read_csv('artifacts/movies_rec_user.csv')
    return recs

recs_df = load_data()

st.set_page_config("Movie Recommender", page_icon="")

st.title("🎬 Movie Recommender")

mode = st.radio(
    "Choose recommendation mode:",
    ("By User ID", "By Movie Title"),
    horizontal=True,
)

if mode == "By User ID":
    user_id = st.number_input("Enter user ID", min_value=1, step=1)

    if st.button("Get Recommendations"):
        users_recs = recs_df[recs_df["userId"] == user_id] 

        if users_recs.empty:
            st.warning("No recommendations for this user.")
        else:
            st.subheader("Recommended movies:")
            for _, row in users_recs.iterrows():
                st.write(f"**{row['title']}**  |  Predicted rating: {row['rating']:.2f}")

if mode=="By Movie Title":

    st.subheader("Movies similar to a given title")
    movie_input = st.text_input("Enter Movie Title")

    if st.button("Find Similar Movies"):
        response = requests.post(
        DATABRICKS_URL,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "movie_title": movie_input,
            "top_n": 10
        }
    )

    results = response.json()

    for movie in results:
        st.write(f"🎬 {movie['title']}  |  Similarity: {movie['similarity']}")