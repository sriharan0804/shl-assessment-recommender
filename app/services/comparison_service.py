from typing import Any

from app.services.catalog_service import load_catalog


def normalize(text: str) -> str:
    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )


def find_matching_assessments(text: str) -> list[dict[str, Any]]:
    text_lower = normalize(text)
    matches = []

    for item in load_catalog():
        name = item.get("name", "")
        normalized_name = normalize(name)

        if normalized_name and normalized_name in text_lower:
            matches.append(item)

    # fallback: token overlap match
    if len(matches) < 2:
        for item in load_catalog():
            if item in matches:
                continue

            name = item.get("name", "")
            name_tokens = set(normalize(name).split())
            text_tokens = set(text_lower.split())

            if name_tokens and len(name_tokens & text_tokens) >= min(2, len(name_tokens)):
                matches.append(item)

            if len(matches) >= 2:
                break

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
        f"- Duration: {first.get('duration') or 'N/A'}\n"
        f"- Remote: {first.get('remote', 'N/A')}\n"
        f"- Adaptive: {first.get('adaptive', 'N/A')}\n"
        f"- Description: {first.get('description', 'No description available')}\n\n"
        f"{second['name']}:\n"
        f"- Type: {second.get('test_type', 'N/A')}\n"
        f"- Duration: {second.get('duration') or 'N/A'}\n"
        f"- Remote: {second.get('remote', 'N/A')}\n"
        f"- Adaptive: {second.get('adaptive', 'N/A')}\n"
        f"- Description: {second.get('description', 'No description available')}\n\n"
        "The key difference is based on their catalog descriptions, assessment type, duration, remote availability, and adaptive setting."
    )