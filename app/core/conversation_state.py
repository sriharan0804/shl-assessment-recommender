from app.models.schemas import Message


def get_user_context(messages: list[Message]) -> str:
    return " ".join(
        message.content for message in messages if message.role == "user"
    )


def get_last_user_message(messages: list[Message]) -> str:
    user_messages = [m.content for m in messages if m.role == "user"]
    return user_messages[-1] if user_messages else ""


def is_vague_query(text: str) -> bool:
    text = text.lower().strip()
    words = text.split()

    vague_phrases = {
        "assessment",
        "i need assessment",
        "i need an assessment",
        "need assessment",
        "need test",
        "i need test",
        "recommend assessment",
        "suggest assessment",
    }

    return text in vague_phrases or len(words) <= 3


def is_refinement(text: str) -> bool:
    text = text.lower()

    refinement_words = [
        "actually",
        "also",
        "add",
        "include",
        "remove",
        "instead",
        "change",
        "update",
        "personality",
        "cognitive",
        "communication",
    ]

    return any(word in text for word in refinement_words)


def is_comparison(text: str) -> bool:
    text = text.lower()

    comparison_words = [
        "compare",
        "difference",
        "different between",
        "vs",
        "versus",
        "which is better",
    ]

    return any(word in text for word in comparison_words)

def is_refinement(text: str) -> bool:
    text = text.lower()

    refinement_words = [
        "actually",
        "also",
        "add",
        "include",
        "remove",
        "instead",
        "change",
        "update",
        "personality",
        "cognitive",
        "ability",
        "communication",
    ]

    return any(word in text for word in refinement_words)

def has_enough_context(text: str) -> bool:
    text = text.lower()

    role_words = [
        "developer", "engineer", "manager", "analyst", "sales",
        "support", "consultant", "graduate", "java", "python",
        "sql", "frontend", "backend", "data"
    ]

    skill_words = [
        "java", "python", "sql", "communication", "stakeholder",
        "personality", "cognitive", "reasoning", "leadership",
        "problem solving", "coding", "database"
    ]

    has_role = any(word in text for word in role_words)
    has_skill = any(word in text for word in skill_words)

    return has_role and has_skill


def clarification_question(text: str) -> str:
    text = text.lower()

    if not any(word in text for word in ["developer", "engineer", "manager", "analyst", "sales"]):
        return "Sure. What role are you hiring for, and what are the key skills you want to assess?"

    if not any(word in text for word in ["entry", "graduate", "mid", "senior", "manager"]):
        return "Got it. What seniority level is this role for: entry-level, graduate, mid-level, senior, or manager?"

    return "Could you share the key skills or traits you want to assess, such as technical skills, reasoning ability, communication, or personality?"