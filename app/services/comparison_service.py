from typing import Any

from app.services.catalog_service import load_catalog


def find_matching_assessments(text: str) -> list[dict[str, Any]]:
    text_lower = text.lower()
    matches = []

    for item in load_catalog():
        name = item.get("name", "")
        if name and name.lower() in text_lower:
            matches.append(item)

    return matches


def compare_assessments(text: str) -> str:
    matches = find_matching_assessments(text)

    if len(matches) < 2:
        return (
            "I can compare assessments using the SHL catalog, but I need the exact "
            "assessment names. Please mention two assessment names from the catalog."
        )

    first, second = matches[0], matches[1]

    return (
        f"Here is a catalog-grounded comparison:\n\n"
        f"{first['name']}:\n"
        f"- Type: {first.get('test_type', 'N/A')}\n"
        f"- Duration: {first.get('duration', 'N/A') or 'N/A'}\n"
        f"- Remote: {first.get('remote', 'N/A')}\n"
        f"- Adaptive: {first.get('adaptive', 'N/A')}\n"
        f"- Description: {first.get('description', 'No description available')}\n\n"
        f"{second['name']}:\n"
        f"- Type: {second.get('test_type', 'N/A')}\n"
        f"- Duration: {second.get('duration', 'N/A') or 'N/A'}\n"
        f"- Remote: {second.get('remote', 'N/A')}\n"
        f"- Adaptive: {second.get('adaptive', 'N/A')}\n"
        f"- Description: {second.get('description', 'No description available')}\n\n"
        "The main difference is based on the catalog descriptions and test type shown above."
    )