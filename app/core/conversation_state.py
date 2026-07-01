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