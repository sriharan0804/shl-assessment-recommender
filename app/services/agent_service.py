from app.models.schemas import ChatRequest , ChatResponse

def handle_chat(request : ChatRequest)-> ChatResponse:
    if not request.messages:
        return ChatResponse(reply = " please tell me what role you are hiring for.",
                            recommendations = [],
                            end_of_conversation = False,
                            )
    last_message = request.messages[-1].content.lower()

    if "assessment" in last_message and len(last_message.split()) <=5:
        return ChatResponse(
            reply = "sure. what role are you hiring for , and what skills should the assessment cover?",
            recommendations =[],
            end_of_conversation = False
        )
    return ChatResponse(
        reply = " Thanks.. I need a bit more context before recommendation SHL assessments.Could you share the role , seniority, and key skills?",
        recommendation = [],
        end_of_conversation = False,
    )