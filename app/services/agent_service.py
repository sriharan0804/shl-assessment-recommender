from app.core.validator import filter_valid_recommendations
from app.models.schemas import ChatRequest, ChatResponse, Recommendation
from app.services.retrieval_service import retrieve_assessments


def handle_chat(request: ChatRequest) -> ChatResponse:
    user_messages = [
        message.content for message in request.messages if message.role == "user"
    ]

    if not user_messages:
        return ChatResponse(
            reply="Please tell me what role you are hiring for.",
            recommendations=[],
            end_of_conversation=False,
        )

    full_context = " ".join(user_messages)
    last_message = user_messages[-1]

    if is_vague(last_message):
        return ChatResponse(
            reply="Sure. What role are you hiring for, and what skills should the assessment cover?",
            recommendations=[],
            end_of_conversation=False,
        )

    retrieved = retrieve_assessments(full_context, limit=10)
    valid_items = filter_valid_recommendations(retrieved)

    if not valid_items:
        return ChatResponse(
            reply="I need a bit more detail to recommend suitable SHL assessments. Could you share the role, seniority, and key skills?",
            recommendations=[],
            end_of_conversation=False,
        )

    recommendations = [
        Recommendation(
            name=item["name"],
            url=item["url"],
            test_type=item["test_type"],
        )
        for item in valid_items[:10]
    ]

    return ChatResponse(
        reply=f"Based on your role requirements, here are {len(recommendations)} SHL assessments that best match the context.",
        recommendations=recommendations,
        end_of_conversation=False,
    )


def is_vague(text: str) -> bool:
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
    }

    return text in vague_phrases or len(words) <= 3