import faiss
import pickle
import numpy as np
import pandas as pd

movies_df = pd.read_csv("data/movies.csv")  # columns: movieId, title, genres
id_to_title = dict(zip(movies_df["movieId"], movies_df["title"]))

movies_df["title_lower"] = movies_df["title"].str.lower()

def find_movie_id_by_name(name: str):
    name = name.strip().lower()
    movies_df["title_clean"] = movies_df["title_lower"].str.replace(
    r"\s*\(\d{4}\)", "", regex=True)

    matches = movies_df[movies_df["title_clean"].str.contains(name, na=False)]

    if matches.empty:
        return None
    # Take the first match
    row = matches.iloc[0]
    print(int(row["movieId"]), row["title"])
    return int(row["movieId"]), row["title"]

# Load index ONCE at startup
index = faiss.read_index("item_factors.faiss")

with open("item_factors.pkl", "rb") as f:
    item_factors_dict = pickle.load(f)  # movie_id -> vector

def get_vector_for_movie(movie_id: int):
    return item_factors_dict[movie_id].reshape(1, -1).astype("float32")

def search_similar(movie_title, k=10):
    res = find_movie_id_by_name(movie_title)
    print("Result res:",res)
    if res is None:
        return "Movie Not Found"
    movie_id, canonical_title = res

    try:
        q_vec = get_vector_for_movie(movie_id)  # shape (1, d)
    except RuntimeError:
        # ID not in index
        return "Movie Not Found in index"

    # 3) search in FAISS
    D, I = index.search(q_vec, k + 1)  # include self
    ids = I[0].tolist()
    scores = D[0].tolist()

    results = []
    for mid, score in zip(ids, scores):
        if mid == movie_id:
            continue  # skip the query movie itself
        title = id_to_title.get(mid, f"Movie {mid}")
        results.append({"movieId": int(mid), "title": title, "score": float(score)})
        if len(results) >= k:
            break

    return {"query_title": canonical_title, "results": results}

print(search_similar("toy story"))
