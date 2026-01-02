import streamlit as st
from inference import search_similar
import pandas as pd

st.set_page_config("Movie Recommender", page_icon="🎬", layout="wide")

@st.cache_data
def load_user_recs():
    return pd.read_csv('artifacts/movies_rec_user.csv')

recs_df = load_user_recs()  # ~10MB, fine

st.title("🎬 Movie Recommender")

mode = st.radio(
    "Choose recommendation mode:",
    ("By User ID", "By Movie Title"),
    horizontal=True,
)

if mode == "By User ID":
    user_id = st.number_input("Enter user ID", min_value=1, step=1)

    if st.button("Get Recommendations"):
        user_recs = recs_df[recs_df["userId"] == user_id]
        if user_recs.empty:
            st.warning("No recommendations for this user.")
        else:
            st.subheader("Recommended movies:")
            for _, row in user_recs.iterrows():
                st.write(f"**{row['title']}** | Predicted rating: {row['rating']:.2f}")

if mode=="By Movie Title":

    st.subheader("Search similar movies")
    movie_input = st.text_input("Enter Movie Title")

    if st.button("Find similar movies") and movie_input:
        res = search_similar(movie_input, k=10)
        if res == "Movie Not Found" or res == "Movie Not Found in index":
            st.error(res)
        else:
            st.write(f"Similar to: **{res['query_title']}**")
            for r in res["results"]:
                st.write(f"- {r['title']} (score: {r['score']:.3f})")