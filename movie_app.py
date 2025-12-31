import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

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

        if users_recs.empty:
            st.warning("No recommendations for this user.")
        else:
            st.subheader("Recommended movies:")
            for _, row in users_recs.iterrows():
                st.write(f"**{row['title']}**  |  Predicted rating: {row['rating']:.2f}")

if mode=="By Movie Title":

    st.subheader("Search similar movies")
    movie_input = st.text_input("Enter Movie Title")

    if st.button("Find Similar Movies"):
        # Note: For true "Similarity", you usually need a pre-trained ALS model 
        # or a Cosine Similarity matrix. 
        # For now, this searches for the movie in your Spark DataFrame:
        similar_movies = recs_df.filter(col("title").contains(movie_input)).limit(10).collect()
        
        if not similar_movies:
            st.error("Movie not found in dataset.")
        else:
            for movie in similar_movies:
                st.write(f"🎬 {movie['title']} | Rating: {movie['rating']}")