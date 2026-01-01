from pyspark.sql import SparkSession

def get_spark():
    return SparkSession.builder \
        .appName("movie_app") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()