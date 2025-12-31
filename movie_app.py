import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from inference import get_similar_movies

@st.cache_resource
def get_spark():
    # We use 'local[*]' to use all available CPU cores in the container
    spark = SparkSession.builder \
        .appName("MovieRec") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    return spark

@st.cache_resource
def load_data():
    spark = get_spark()
    recs = spark.read.csv('artifacts/movies_rec_user.csv',header=True, inferSchema=True)
    return recs

spark = get_spark()
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
        users_recs = recs_df.filter(col("userId") == user_id).collect()

        if not users_recs:
            st.warning("No recommendations for this user.")
        else:
            st.subheader("Recommended movies:")
            for row in users_recs:
                st.write(f"**{row['title']}**  |  Predicted rating: {row['rating']:.2f}")

if mode=="By Movie Title":

    st.subheader("Search similar movies")
    movie_input = st.text_input("Enter Movie Title")
    results = get_similar_movies(movie_input)
    if st.button("Find Similar Movies"):
        if results == "Movie Not Found":
            st.error("Could not find that movie. Try a different name!")
        elif results == "Empty Input":
            st.warning("Please enter a movie title.")
        else:
            for movie in results:
                st.write(f"🎬 {movie['title']} | Similarity: {movie['similarity']}")