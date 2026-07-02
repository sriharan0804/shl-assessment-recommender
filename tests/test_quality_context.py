from app.core.query_context import extract_query_context


def test_extract_query_context():
    context = extract_query_context(
        "Hiring a graduate Java developer. Need remote English assessment under 30 minutes with reasoning."
    )

    assert context.role is not None
    assert "java" in context.skills
    assert context.seniority == "graduate"
    assert context.language == "english"
    assert context.remote is True
    assert context.max_duration == 30
    assert context.wants_ability is True