import pickle
import faiss
import numpy as np

def load_vectors_from_pickle(path="item_factors.pkl"):
    with open(path, "rb") as f:
        item_factors = pickle.load(f) 

    ids = np.array(list(item_factors.keys()), dtype=np.int64)
    vectors = np.stack([item_factors[i] for i in ids]).astype("float32")  # shape (N, d)
    return ids, vectors

ids, vectors = load_vectors_from_pickle("item_factors.pkl")
d = vectors.shape[1]

faiss.normalize_L2(vectors)

index = faiss.IndexFlatIP(d)        # or IndexFlatL2 for Euclidean [web:191][web:202]
index = faiss.IndexIDMap(index)     # allow custom IDs

index.add_with_ids(vectors, ids)

faiss.write_index(index, "item_factors.faiss")
print("🎉")