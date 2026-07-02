def rank_assessments(items: list[dict], query: str) -> list[dict]:
    query = query.lower()

    def score(item: dict) -> int:
        text = item.get("search_text", "").lower()
        name = item.get("name", "").lower()
        test_type = item.get("test_type", "")

        s = 0

        # skill/name matches
        for word in query.split():
            if word in name:
                s += 5
            elif word in text:
                s += 2

        # role-based boosts
        if any(w in query for w in ["java", "developer", "programmer", "software"]):
            if test_type == "K":
                s += 5

        if any(w in query for w in ["stakeholder", "communication", "customer"]):
            if test_type in {"P", "C"}:
                s += 4

        if any(w in query for w in ["graduate", "entry", "freshers", "fresher"]):
            if "graduate" in text or "entry-level" in text:
                s += 4

        if any(w in query for w in ["manager", "leadership", "supervisor"]):
            if "manager" in text or "leadership" in text:
                s += 4

        if any(w in query for w in ["cognitive", "aptitude", "reasoning", "ability"]):
            if test_type == "A":
                s += 5

        if any(w in query for w in ["personality", "behavior", "behaviour"]):
            if test_type == "P":
                s += 6

        return s

    return sorted(items, key=score, reverse=True)