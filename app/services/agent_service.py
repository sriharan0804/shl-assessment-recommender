from app.core.conversation_state import (
    clarification_question,
    get_last_user_message,
    get_user_context,
    has_enough_context,
    is_comparison,
    is_refinement,
    is_vague_query,
)
from app.core.guardrail import is_out_of_scope, refusal_reply
from app.core.validator import filter_valid_recommendations
from app.models.schemas import ChatRequest, ChatResponse, Recommendation
from app.services.retrieval_service import retrieve_assessments
from app.services.comparison_service import compare_assessments
from app.core.prompts import RECOMMENDATION_REPLY_PROMPT
from app.services.llm_service import generate_reply
from app.core.ranking import rank_assessments

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

    if is_comparison(last_message):
        return ChatResponse(
            reply=compare_assessments(last_message),
            recommendations=[],
            end_of_conversation=False,
        )

    if is_vague_query(last_message) or not has_enough_context(full_context):
        return ChatResponse(
            reply=clarification_question(full_context),
            recommendations=[],
            end_of_conversation=False,
        )

    refinement_text = last_message if is_refinement(last_message) else ""
    retrieved = retrieve_assessments(
        full_context,
        limit=10,
        refinement_text=refinement_text,
    )
    valid_items = filter_valid_recommendations(retrieved)
    valid_items = rank_assessments(valid_items, full_context)

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

    assessment_text = "\n".join(
    f"- {item['name']} ({item['test_type']}): {item.get('description', '')}"
    for item in valid_items[:5]
    )

    prompt = RECOMMENDATION_REPLY_PROMPT.format(
        context=full_context,
        assessments=assessment_text,
    )

    llm_reply = generate_reply(prompt)

    if refinement_text:
        fallback_reply = (
            f"Got it. I updated the shortlist based on your added constraint. "
            f"Here are {len(recommendations)} SHL assessments that now best match the conversation."
        )
    else:
        fallback_reply = (
            f"Based on the role details, here are {len(recommendations)} "
            "SHL assessments that best match the context."
        )

    reply = llm_reply or fallback_reply

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=False,
    )