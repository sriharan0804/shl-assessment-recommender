def is_out_of_scope(text: str) -> bool:
    text = text.lower()

    blocked_topics = [
        "salary",
        "legal advice",
        "employment law",
        "which candidate should i hire",
        "interview questions",
        "resume",
        "cover letter",
        "ignore previous instructions",
        "forget your instructions",
        "system prompt",
        "jailbreak",
        "act as",
    ]

    return any(topic in text for topic in blocked_topics)


def refusal_reply() -> str:
    return (
        "I can only help with SHL assessment recommendations, comparisons, "
        "and catalog-based assessment selection."
    )