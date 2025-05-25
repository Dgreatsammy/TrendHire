from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)  # Vector size for the above model
id_map = []

def add_to_index(text, id):
    vector = model.encode([text])
    index.add(np.array(vector).astype("float32"))
    id_map.append(id)

def search(query, top_k=5):
    vector = model.encode([query])
    D, I = index.search(np.array(vector).astype("float32"), top_k)
    return [id_map[i] for i in I[0]]
