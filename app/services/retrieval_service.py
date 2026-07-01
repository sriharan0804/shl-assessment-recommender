import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.services.catalog_service import load_catalog


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def load_vector_index():
    index_path = Path(settings.vector_index_path)

    if not index_path.exists():
        return None

    return faiss.read_index(str(index_path))


@lru_cache(maxsize=1)
def load_vector_metadata() -> list[dict[str, Any]]:
    metadata_path = Path(settings.vector_metadata_path)

    if not metadata_path.exists():
        return []

    with metadata_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_assessments(query: str, limit: int = 10) -> list[dict[str, Any]]:
    semantic_results = semantic_search(query, limit=limit)
    keyword_results = keyword_search(query, limit=limit)

    merged = merge_results(semantic_results, keyword_results)

    return merged[:limit]


def semantic_search(query: str, limit: int = 10) -> list[dict[str, Any]]:
    index = load_vector_index()
    metadata = load_vector_metadata()

    if index is None or not metadata:
        return []

    model = get_embedding_model()
    query_embedding = model.encode([query], normalize_embeddings=True)
    query_embedding = np.array(query_embedding).astype("float32")

    scores, indices = index.search(query_embedding, limit)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(metadata):
            results.append(metadata[idx])

    return results


def keyword_search(query: str, limit: int = 10) -> list[dict[str, Any]]:
    query_words = set(query.lower().split())
    catalog = load_catalog()

    scored = []

    for item in catalog:
        search_text = item.get("search_text", "").lower()
        name = item.get("name", "").lower()

        score = 0

        for word in query_words:
            if word in search_text:
                score += 1
            if word in name:
                score += 3

        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in scored[:limit]]


def merge_results(
    semantic_results: list[dict[str, Any]],
    keyword_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    seen = set()
    merged = []

    for item in keyword_results + semantic_results:
        url = item.get("url")
        if url and url not in seen:
            seen.add(url)
            merged.append(item)

    return merged