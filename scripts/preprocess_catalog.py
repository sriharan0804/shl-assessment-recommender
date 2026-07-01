import json
from pathlib import Path


RAW_PATH = Path("data/raw_catalog.json")
PROCESSED_PATH = Path("data/processed_catalog.json")


def normalize_item(item: dict) -> dict:
    return {
        "entity_id": item.get("entity_id", ""),
        "name": item.get("name", "").strip(),
        "url": item.get("link", "").strip(),
        "test_type": infer_test_type(item.get("keys", [])),
        "description": item.get("description", "").strip(),
        "job_levels": item.get("job_levels", []),
        "languages": item.get("languages", []),
        "duration": item.get("duration", ""),
        "remote": item.get("remote", ""),
        "adaptive": item.get("adaptive", ""),
        "keys": item.get("keys", []),
        "search_text": build_search_text(item),
    }


def infer_test_type(keys: list[str]) -> str:
    joined = " ".join(keys).lower()

    if "knowledge" in joined or "skills" in joined:
        return "K"
    if "personality" in joined or "behavior" in joined:
        return "P"
    if "ability" in joined or "aptitude" in joined:
        return "A"
    if "situational" in joined or "judgment" in joined:
        return "S"
    if "competencies" in joined:
        return "C"

    return "O"


def build_search_text(item: dict) -> str:
    parts = [
        item.get("name", ""),
        item.get("description", ""),
        " ".join(item.get("job_levels", [])),
        " ".join(item.get("languages", [])),
        " ".join(item.get("keys", [])),
        item.get("duration", ""),
        item.get("remote", ""),
        item.get("adaptive", ""),
    ]

    return " ".join(parts).lower()


def main():
    with RAW_PATH.open("r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    content = "".join(
        ch for ch in content
        if ch >= " " or ch in "\n\r\t"
    )

    raw_data = json.loads(content)

    processed = []

    for item in raw_data:
        if item.get("status") != "ok":
            continue

        if not item.get("name") or not item.get("link"):
            continue

        processed.append(normalize_item(item))

    with PROCESSED_PATH.open("w", encoding="utf-8") as file:
        json.dump(processed, file, indent=2, ensure_ascii=False)

    print(f"Processed {len(processed)} catalog items")
    print(f"Saved to {PROCESSED_PATH}")


if __name__ == "__main__":
    main()