import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


CATALOG_PATH = Path("data/processed_catalog.json")
INDEX_PATH = Path("data/vector_index/index.faiss")
METADATA_PATH = Path("data/vector_index/metadata.json")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    with CATALOG_PATH.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    texts = [item.get("search_text", "") for item in catalog]

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, normalize_embeddings=True)
    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    with METADATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(catalog, file, indent=2, ensure_ascii=False)

    print(f"Built FAISS index with {len(catalog)} items")


if __name__ == "__main__":
    main()