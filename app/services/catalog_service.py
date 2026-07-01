import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.config import settings

@lru_cache(maxsize = 1)
def load_catalog() -> list[dict[str , Any]]:
    path = Path(settings.catalog_path)
    if not path.exists():
        return []
    with path.open("r" , encoding = "utf-8") as file:
        data = json.load(file)
    return data if isinstance(data , list) else []

def get_catalog_urls() -> set[str]:
    return {item['url'] for item in load_catalog() if item.get("url")}

def get_catalog_names() -> set[str]:
    return {item["name"] for item in load_catalog() if item.get("name")}

def find_by_name(name:str) -> set[str , Any]:
    target = name.lower().strip()

    for item in load_catalog():
        if item.get("name","").lower().strip() == target:
            return item
    return None    