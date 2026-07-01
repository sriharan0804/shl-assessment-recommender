from app.core.conversation_state import (
    get_last_user_message,
    get_user_context,
    is_comparison,
    is_vague_query,
)
from app.core.guardrail import is_out_of_scope, refusal_reply
from app.core.validator import filter_valid_recommendations
from app.models.schemas import ChatRequest, ChatResponse, Recommendation
from app.services.retrieval_service import retrieve_assessments
from app.services.comparison_service import compare_assessments

def handle_chat(request: ChatRequest) -> ChatResponse:
    full_context = get_user_context(request.messages)
    last_message = get_last_user_message(request.messages)

    if not last_message:
        return ChatResponse(
            reply="Please tell me what role you are hiring for.",
            recommendations=[],
            end_of_conversation=False,
        )

    if is_out_of_scope(last_message):
        return ChatResponse(
            reply=refusal_reply(),
            recommendations=[],
            end_of_conversation=False,
        )

    if is_vague_query(last_message):
        return ChatResponse(
            reply="Sure. What role are you hiring for, and what skills should the assessment cover?",
            recommendations=[],
            end_of_conversation=False,
        )

    if is_comparison(last_message):
        return ChatResponse(
            reply=compare_assessments(last_message),
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

    reply = (
        f"Based on the role details, here are {len(recommendations)} "
        "SHL assessments that best match the context."
    )

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=False,
    )