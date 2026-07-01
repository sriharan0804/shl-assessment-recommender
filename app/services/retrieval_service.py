from typing import Any

from app.services.catalog_service import load_catalog

def retrieve_assessments(query: str , limit: int =10)-> list[dict[str , Any]]:
    query_words = set(query.lower().strip())
    catalog = load_catalog()

    scored = []

    for item in catalog:
        search_text = item.get("search_text" , "").lower()
        score = 0
        for word in query_words:
            if word in search_text:
                score += 1
        
        #it will boost extra match in assessment name
        name = item.get("name" , "").lower()
        for word in query_words:
            if word in name:
                score += 3

        if score > 0:
            scored.append((score , item))

    scored.sort(key = lambda x: x[0] , reverse = True)
    return [item for score , item in scored[: limit]]