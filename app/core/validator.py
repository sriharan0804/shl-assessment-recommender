from app.services.catalog_service import get_catalog_urls

def filter_valid_recommendations(items : list[dict]) -> list[dict]:
    valid_urls = get_catalog_urls()

    return [
        item for item in items
        if item.get("name") and item.get("url") in valid_urls
    ]