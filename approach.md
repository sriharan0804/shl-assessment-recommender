```rust
# SHL Conversational Assessment Recommender

## 1. Problem Understanding

- The goal of this project is to build a conversational assistant that helps
hiring managers identify the most suitable SHL Individual Test Solutions 
through natural language conversations. In practice, recruiters often begin 
with incomplete or high-level requirements rather than a precise list of
assessments. Instead of expecting users to know the SHL catalog, the 
assistant gradually gathers the required information through conversation 
and recommends relevant assessments based on the official SHL product catalog.

- To meet the assignment requirements, the system is designed around four core 
conversational behaviors. It asks follow-up questions when the initial request 
is too vague, recommends a shortlist of one to ten assessments once sufficient 
information is available, updates recommendations when the user's requirements 
change during the conversation, and compares multiple SHL assessments using 
only information available in the catalog.

- The API follows a stateless design, where each request contains the complete 
conversation history. This removes the need for server-side session management 
while allowing the agent to reconstruct the conversation context for every 
request. Besides matching the required API specification, this approach keeps 
the service simple to deploy and easy to scale.

- One of the primary design goals throughout the project was to ensure that 
recommendations remain trustworthy and grounded. The language model is used to 
understand user intent and generate conversational responses, but it is never 
allowed to invent assessment names or URLs. Every recommendation is retrieved 
from the processed SHL catalog and validated before being returned. This 
guarantees that all assessment names,

```

```rust

                    User
                      │
                      ▼
              FastAPI (/chat)
                      │
                      ▼
               Agent Service
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Guardrails     Query Context      Intent Detection
                      │
                      ▼
             Hybrid Retrieval
      (Keyword + Semantic Search)
                      │
                      ▼
              Ranking Engine
                      │
                      ▼
          Catalog Validation
                      │
                      ▼
             JSON Response



## 2. System Design

- The system follows a modular architecture to keep individual responsibilities 
separated and make the implementation easier to extend and maintain. The 
application is exposed through a FastAPI service that provides the two required 
endpoints: `/health` for readiness checks and `/chat` for conversational 
recommendations.

- When a request reaches the `/chat` endpoint, the complete conversation history 
is passed to the Agent Service. Since the API is stateless, the agent 
reconstructs the conversation context from the supplied messages instead of 
relying on any server-side session.

- The first stage of processing applies guardrails to ensure that the request is 
within the supported scope. Requests unrelated to SHL assessments, 
prompt-injection attempts, or requests that would require information outside 
the SHL catalog are safely refused.

- For valid requests, a query context is extracted from the conversation. This 
component identifies structured information such as job role, required skills, 
seniority level, preferred language, assessment duration, remote or adaptive 
preferences, and other relevant constraints. Converting free-form conversation 
into structured attributes simplifies downstream retrieval and ranking.

- The retrieval layer uses a hybrid strategy that combines keyword matching with 
semantic search over the processed SHL catalog. The retrieved candidates are 
then passed through a ranking engine, which scores assessments using both 
semantic relevance and catalog-specific signals such as job level, assessment 
type, language availability, duration, and other user preferences.

- Before returning a response, every recommended assessment is validated against 
the processed SHL catalog. This validation step guarantees that the system only 
returns legitimate assessment names and official SHL URLs, preventing hallucinated 
recommendations and ensuring that every response remains grounded in catalog data.
```

```rust


                  User Query
                       │
                       ▼
          Query Context Extraction
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 Keyword Retrieval             Semantic Retrieval
        │                             │
        └──────────────┬──────────────┘
                       ▼
              Candidate Merging
                       ▼
               Ranking Engine
                       ▼
            Catalog Validation
                       ▼
             Top 1–10 Results

## 3 . Retrieval Strategy

- The recommendation quality largely depends on how relevant assessments are 
retrieved from the SHL catalog. Instead of relying solely on a language model, 
I designed a hybrid retrieval pipeline that combines structured catalog search 
with semantic understanding. This approach improves recommendation quality 
while ensuring that every returned assessment exists in the official SHL 
catalog.

- The retrieval process begins by extracting structured information from the 
user's conversation. The query context extractor identifies attributes such as 
job role, technical skills, seniority level, preferred language, assessment 
duration, remote or adaptive preferences, and any additional constraints 
mentioned by the user. Converting conversational text into structured 
information allows the retrieval pipeline to understand hiring requirements 
more accurately.

- Using the extracted context, the system performs hybrid retrieval in two stages. 
First, keyword-based retrieval searches the processed SHL catalog for exact 
matches on assessment names, skills, job roles, competencies, and other catalog
metadata. In parallel, semantic retrieval searches the vector index to identify 
assessments that are conceptually similar to the user's requirements, even when 
the wording differs from the catalog.

- The candidate assessments returned by both retrieval methods are merged into a 
single candidate set. A ranking engine then orders the candidates using 
multiple catalog-specific signals, including keyword relevance, job level 
compatibility, assessment category, language availability, assessment duration, 
remote and adaptive support, and user preferences collected during the conversation. 
This additional ranking step helps prioritize the most relevant assessments rather 
than simply returning the first retrieved results.

- Finally, every recommendation passes through a validation layer before being 
included in the response. The validation step verifies that the assessment 
exists in the processed SHL catalog and that the returned URL matches an 
official SHL catalog entry. This prevents hallucinated assessment names or 
invalid URLs and ensures that every recommendation is grounded in catalog data.

```

```rust
## 4 . Conversation Management

- The conversational agent is designed to support multiple interaction patterns 
while remaining stateless. Instead of storing conversation state on the server, 
each request contains the complete conversation history, allowing the agent to 
reconstruct the context before making a decision.

- The first step is intent identification. Based on the latest user message and 
the previous conversation history, the agent determines whether the user is 
requesting a new recommendation, refining an existing shortlist, comparing 
assessments, or asking an unrelated question. This routing allows different 
processing logic to be applied without increasing the complexity of the API.

- For recommendation requests, the agent first checks whether sufficient 
information is available. If important details such as job role, seniority, or 
required skills are missing, it asks targeted follow-up questions instead of 
making assumptions. Once enough context has been collected, the retrieval and 
ranking pipeline generates a grounded shortlist of assessments.

- If the user modifies the requirements during the conversation—for example by 
adding personality assessments or changing the target role—the agent 
reconstructs the updated context from the conversation history and generates a 
revised shortlist rather than starting the conversation again.

- The comparison workflow retrieves the requested assessments from the SHL 
catalog and generates a comparison using catalog information only. Throughout 
the conversation, the agent avoids making unsupported assumptions and only 
produces recommendations after sufficient context has been gathered.

```

```rust
## 5. Evaluation Strategy

- To verify the correctness of the implementation, I tested the system at both 
the API and conversational levels. Unit tests were written for the major 
components, including the health endpoint, response schema, catalog validation, clarification behavior, recommendation generation, refinement handling, 
comparison requests, and guardrails. Running these tests throughout development 
helped identify regressions whenever new features were added.

- Beyond unit testing, I manually evaluated the conversational flow using 
different hiring scenarios. These included vague requests that required 
clarification, detailed job descriptions, mid-conversation requirement changes, 
assessment comparison requests, and off-topic or prompt-injection attempts. 
Testing a variety of conversation patterns helped verify that the agent behaved 
consistently instead of only working for a single happy path.

- Special attention was given to response validation. Every recommendation 
returned by the API is checked against the processed SHL catalog to ensure that 
the assessment name and URL are valid. This additional validation layer reduces 
the possibility of hallucinated recommendations and guarantees that responses 
remain grounded in official catalog data.

- Finally, the API was validated against the required assignment schema to 
ensure that every response contains the expected fields 
(`reply`, `recommendations`, and `end_of_conversation`) while maintaining the 
stateless request format specified in the assessment.




```

```rust
## 6. Challenges, Trade-offs & Future Improvements

- One of the main challenges during development was balancing conversational 
flexibility with reliable recommendations. While a language model is effective 
at understanding natural language, relying on it alone can lead to hallucinated 
assessment names or inconsistent recommendations. To address this, I designed 
the system so that the language model focuses on conversational understanding, 
while retrieval, ranking, and validation remain grounded in the SHL catalog.

- Another challenge was handling incomplete user requirements. Recruiters often 
describe roles with limited information, making it necessary to determine when 
the system should ask follow-up questions instead of immediately generating 
recommendations. Implementing a clarification-first workflow significantly 
improved the quality of the final shortlist.


- Given the project timeline, the focus was on building a reliable and 
maintainable solution that satisfies the assignment requirements. Some 
advanced features, such as learning-to-rank models, feedback-driven 
personalization, and more sophisticated semantic reranking, were intentionally 
left out to keep the system simple, explainable, and robust.

- In future iterations, I would further improve retrieval quality by 
incorporating stronger embedding models, dedicated reranking models, and more 
comprehensive evaluation using larger conversational datasets. These 
enhancements would improve recommendation accuracy while preserving the same 
grounded and stateless architecture.

```