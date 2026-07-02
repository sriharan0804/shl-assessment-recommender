from app.services.catalog_service import get_catalog_urls


def filter_valid_recommendations(items: list[dict]) -> list[dict]:
    valid_urls = get_catalog_urls()

    valid_items = []
    seen_urls = set()

    for item in items:
        url = item.get("url")

        if not item.get("name"):
            continue

        if url not in valid_urls:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)
        valid_items.append(item)

    return valid_items