from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.feature import Normalizer
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql.types import DoubleType, ArrayType
from pyspark.sql.functions import explode, split, udf

@staticmethod
def get_spark():
    return SparkSession.builder \
        .appName("movie_app") \
        .master("local[*]") \
        .getOrCreate()

# Function to find similar movies using cosine similarity
def get_similar_movies(movie_title, top_n=10):
    spark = get_spark()
    movies = spark.read.csv("data/movies.csv", header=True, inferSchema=True)

    # Extract all unique genres from movies
    all_genres = movies.select(explode(split("genres", "\\|")).alias("genre")).distinct()
    genres_list = [row.genre for row in all_genres.collect()]  # Pure Python list
    
    genres_broadcast = spark.sparkContext.broadcast(genres_list)

    # Convert genre string to binary vector (UDF)
    def genre_to_vector(genres_str):
        if genres_str is None:
            return [0.0] * len(genres_broadcast.value)
        genres = set(genres_str.split("|"))
        return [1.0 if g in genres else 0.0 for g in genres_broadcast.value]

    vector_udf = udf(genre_to_vector, ArrayType(DoubleType()))

    # apply genre vector udf
    movies_with_vectors = movies.withColumn("genre_vector", vector_udf("genres"))

    # Convert to proper Vector type (simplified - use ML VectorAssembler for production)
    movies_genre_vec = movies_with_vectors

    as_vector_udf = F.udf(lambda l: Vectors.dense(l), VectorUDT())

    # Normalize vectors (required for cosine similarity)
    df_fixed = movies_genre_vec.withColumn("genre_vector", as_vector_udf(F.col("genre_vector")))
    normalizer = Normalizer(inputCol="genre_vector", outputCol="norm_vectors", p=2.0)
    df_norm = normalizer.transform(df_fixed)

    # Find the movie entered by user
    matched_movie = df_norm.filter(F.col("title").ilike(f"%{movie_title}%")).select("movieId").collect()
    if not matched_movie:
        return "Movie Not Found"

    movie_id = matched_movie[0]["movieId"]
    movie_row = df_norm.filter(F.col("movieId") == movie_id).select("norm_vectors").collect()
    movie_vector = movie_row[0]["norm_vectors"]

    # Cosine similarity = dot product of normalized vectors
    def cosine_similarity(v):
        return float(movie_vector.dot(v))
    
    dot_udf = F.udf(cosine_similarity, DoubleType())

    # Compute similarity with all movies
    recommendations = (df_norm
        .withColumn("similarity", dot_udf(F.col("norm_vectors")))
        .orderBy(F.col("similarity").desc())
        .limit(top_n + 1)
        .select("movieId", "title", F.round(F.col("similarity"), 3).alias("similarity")))
  
    return recommendations