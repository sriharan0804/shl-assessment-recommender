import re
from app.core.query_context import extract_query_context

def rank_assessments(items: list[dict], query: str) -> list[dict]:
    query = query.lower()
    context = extract_query_context(query)

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

        # remote preference
        if "remote" in query:
            if item.get("remote", "").lower() == "yes":
                s += 4

        # adaptive preference
        if "adaptive" in query:
            if item.get("adaptive", "").lower() == "yes":
                s += 4

        # duration preference
        if "short" in query or "quick" in query or "under 30" in query:
            duration = item.get("duration", "").lower()
            if any(minute in duration for minute in ["10", "15", "20", "25", "30"]):
                s += 4

        # language preference
        languages = " ".join(item.get("languages", [])).lower()

        if "english" in query:
            if "english" in languages:
                s += 3

        if "spanish" in query:
            if "spanish" in languages:
                s += 3

        if "french" in query:
            if "french" in languages:
                s += 3

                # job level preference
        job_levels = " ".join(item.get("job_levels", [])).lower()

        if any(w in query for w in ["entry", "entry-level", "fresher", "freshers"]):
            if "entry-level" in job_levels or "graduate" in job_levels:
                s += 4

        if "graduate" in query:
            if "graduate" in job_levels:
                s += 4

        if any(w in query for w in ["mid", "mid-level", "mid professional", "mid-professional"]):
            if "mid-professional" in job_levels:
                s += 4

        if any(w in query for w in ["manager", "lead", "leadership"]):
            if "manager" in job_levels or "supervisor" in job_levels:
                s += 4

        if context.remote and item.get("remote", "").lower() == "yes":
            s += 4

        if context.adaptive and item.get("adaptive", "").lower() == "yes":
            s += 4

        if context.language:
            languages = " ".join(item.get("languages", [])).lower()
            if context.language in languages:
                s += 3

        if context.seniority:
            job_levels = " ".join(item.get("job_levels", [])).lower()
            if context.seniority in job_levels:
                s += 4

        if context.max_duration:
            duration_text = item.get("duration", "").lower()
            nums = re.findall(r"\d+", duration_text)
            if nums and int(nums[0]) <= context.max_duration:
                s += 4

        if context.wants_personality and test_type == "P":
            s += 6

        if context.wants_ability and test_type == "A":
            s += 6

        return s

    return sorted(items, key=score, reverse=True)