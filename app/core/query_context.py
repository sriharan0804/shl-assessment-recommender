from dataclasses import dataclass, field
import re


@dataclass
class QueryContext:
    role: str | None = None
    skills: list[str] = field(default_factory=list)
    seniority: str | None = None
    language: str | None = None
    remote: bool = False
    adaptive: bool = False
    max_duration: int | None = None
    wants_personality: bool = False
    wants_ability: bool = False


def extract_query_context(text: str) -> QueryContext:
    text_lower = text.lower()

    context = QueryContext()

    role_keywords = [
        "developer", "engineer", "manager", "analyst", "consultant",
        "sales", "support", "frontend", "backend", "data scientist",
        "software engineer", "java developer", "python developer"
    ]

    for role in role_keywords:
        if role in text_lower:
            context.role = role
            break

    skill_keywords = [
        "java", "python", "sql", ".net", "javascript", "react",
        "communication", "stakeholder", "leadership", "reasoning",
        "problem solving", "coding", "database", "personality",
        "cognitive", "aptitude"
    ]

    context.skills = [skill for skill in skill_keywords if skill in text_lower]

    if any(w in text_lower for w in ["entry", "entry-level", "fresher", "freshers"]):
        context.seniority = "entry-level"
    elif "graduate" in text_lower:
        context.seniority = "graduate"
    elif any(w in text_lower for w in ["mid", "mid-level", "mid professional"]):
        context.seniority = "mid-professional"
    elif any(w in text_lower for w in ["senior", "experienced"]):
        context.seniority = "senior"
    elif "manager" in text_lower:
        context.seniority = "manager"

    if "english" in text_lower:
        context.language = "english"
    elif "spanish" in text_lower:
        context.language = "spanish"
    elif "french" in text_lower:
        context.language = "french"

    context.remote = "remote" in text_lower
    context.adaptive = "adaptive" in text_lower

    duration_match = re.search(r"under\s+(\d+)\s*(minutes|min|mins)?", text_lower)
    if duration_match:
        context.max_duration = int(duration_match.group(1))
    elif "quick" in text_lower or "short" in text_lower:
        context.max_duration = 30

    context.wants_personality = any(
        w in text_lower for w in ["personality", "behavior", "behaviour"]
    )

    context.wants_ability = any(
        w in text_lower for w in ["cognitive", "aptitude", "reasoning", "ability"]
    )

    return context
