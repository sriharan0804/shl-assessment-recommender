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
def load_faiss_index():
    path = Path(settings.vector_index_path)

    if not path.exists():
        return None

    return faiss.read_index(str(path))


@lru_cache(maxsize=1)
def load_metadata() -> list[dict[str, Any]]:
    path = Path(settings.vector_metadata_path)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_assessments(
    query: str,
    limit: int = 10,
    refinement_text: str = "",
) -> list[dict[str, Any]]:
    keyword_results = keyword_search(query, limit=limit * 2)
    semantic_results = semantic_search(query, limit=limit * 2)

    merged = merge_results(keyword_results, semantic_results)

    if refinement_text:
        merged = apply_refinement_boost(merged, refinement_text)

    return merged[:limit]


def keyword_search(query: str, limit: int = 20) -> list[dict[str, Any]]:
    query_words = set(query.lower().split())
    scored = []

    for item in load_catalog():
        search_text = item.get("search_text", "").lower()
        name = item.get("name", "").lower()

        score = 0

        for word in query_words:
            if word in name:
                score += 4
            elif word in search_text:
                score += 1

        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[:limit]]


def semantic_search(query: str, limit: int = 20) -> list[dict[str, Any]]:
    index = load_faiss_index()
    metadata = load_metadata()

    if index is None or not metadata:
        return []

    model = get_embedding_model()
    query_vector = model.encode([query], normalize_embeddings=True)
    query_vector = np.asarray(query_vector, dtype="float32")

    _, indices = index.search(query_vector, limit)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(metadata):
            results.append(metadata[idx])

    return results


def merge_results(
    keyword_results: list[dict[str, Any]],
    semantic_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged = []
    seen_urls = set()

    # keyword first because exact skill/catalog-name matching is very important
    for item in keyword_results + semantic_results:
        url = item.get("url")
        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        merged.append(item)

    return merged


def apply_refinement_boost(
    items: list[dict[str, Any]],
    refinement_text: str,
) -> list[dict[str, Any]]:
    text = refinement_text.lower()

    def score(item: dict[str, Any]) -> int:
        item_text = item.get("search_text", "").lower()
        test_type = item.get("test_type", "")

        boost = 0

        if "personality" in text and test_type == "P":
            boost += 10

        if ("cognitive" in text or "ability" in text) and test_type == "A":
            boost += 10

        if "communication" in text and "communication" in item_text:
            boost += 7

        return boost

    return sorted(items, key=score, reverse=True)