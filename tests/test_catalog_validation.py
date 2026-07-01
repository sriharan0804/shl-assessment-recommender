from app.services.catalog_service import get_catalog_urls, load_catalog


def test_catalog_loaded():
    catalog = load_catalog()

    assert isinstance(catalog, list)
    assert len(catalog) > 0


def test_catalog_items_have_required_fields():
    catalog = load_catalog()

    for item in catalog:
        assert item.get("name")
        assert item.get("url")
        assert item.get("test_type")
        assert item.get("description") is not None


def test_catalog_urls_are_unique():
    urls = get_catalog_urls()

    assert len(urls) > 0
    assert len(urls) == len(set(urls))