```rust
# SHL Conversational Assessment Recommender

## 1. Problem Understanding

The goal of this project is to build a conversational assistant that helps hiring managers find suitable **SHL Individual Test Solutions** based on natural language requirements.

Recruiters may not always know the exact SHL assessment name. They may describe a role, required skills, seniority level, or hiring need in plain English. The assistant converts this conversation into structured requirements and recommends relevant assessments from the official SHL catalog.

### Key Objectives

* Understand hiring requirements from natural language conversations.
* Ask follow-up questions when the user request is vague or incomplete.
* Recommend a shortlist of **1 to 10 SHL assessments** when enough information is available.
* Update recommendations when the user changes or adds new requirements.
* Compare multiple SHL assessments using catalog-grounded information.
* Prevent hallucinated assessment names or invalid URLs.

### Core Design Idea

The system uses the language model for conversation understanding, but it does not rely on the model alone for recommendations.

Instead:

* User intent is understood through the conversation.
* Relevant assessments are retrieved from the processed SHL catalog.
* Results are ranked using catalog metadata and user constraints.
* Every recommendation is validated before being returned.

This ensures that the assistant remains conversational while keeping recommendations trustworthy and grounded in official SHL catalog data.

### High-Level Flow

```text
User
  |
  v
FastAPI /chat endpoint
  |
  v
Agent Service
  |
  +--> Guardrails
  |
  +--> Query Context Extraction
  |
  +--> Intent Detection
  |
  v
Hybrid Retrieval
(Keyword Search + Semantic Search)
  |
  v
Ranking Engine
  |
  v
Catalog Validation
  |
  v
JSON Response
```

### API Design Decision

The API follows a **stateless design**. Each `/chat` request contains the complete conversation history, allowing the agent to reconstruct context without storing server-side sessions.

This makes the service:

* Easier to deploy
* Easier to scale
* Simpler to test
* Aligned with the required API specification

```

```rust
## 2. System Design

The system follows a modular architecture where each component has a well-defined responsibility. This separation improves maintainability, simplifies testing, and allows individual modules to evolve independently without affecting the overall workflow.

### Architecture Components

| Component                   | Responsibility                                                                                 |
| --------------------------- | ---------------------------------------------------------------------------------------------- |
| **FastAPI Service**         | Exposes the `/health` and `/chat` endpoints.                                                   |
| **Agent Service**           | Orchestrates the complete recommendation workflow.                                             |
| **Guardrails**              | Filters unsupported requests, prompt injections, and off-topic conversations.                  |
| **Intent Detection**        | Determines whether the user wants recommendations, refinements, comparisons, or clarification. |
| **Query Context Extractor** | Converts conversational input into structured hiring requirements.                             |
| **Hybrid Retrieval Engine** | Retrieves relevant assessments using both keyword and semantic search.                         |
| **Ranking Engine**          | Scores and orders candidate assessments based on relevance and user preferences.               |
| **Catalog Validator**       | Ensures every recommendation exists in the official SHL catalog before returning it.           |

---

### Request Processing Workflow

When a request reaches the `/chat` endpoint, the complete conversation history is forwarded to the **Agent Service**. Since the API is stateless, the agent reconstructs the conversation context from the supplied messages instead of relying on server-side sessions.

The request then passes through the following stages:

1. **Guardrails**

   * Detect off-topic requests
   * Reject prompt injection attempts
   * Restrict responses to SHL assessment recommendations

2. **Intent Detection**

   * New recommendation request
   * Follow-up clarification
   * Recommendation refinement
   * Assessment comparison

3. **Query Context Extraction**

   * Job role
   * Required skills
   * Seniority level
   * Assessment duration
   * Language preference
   * Remote or adaptive requirements
   * Additional hiring constraints

4. **Hybrid Retrieval**

   * Keyword search over the processed SHL catalog
   * Semantic similarity search using vector embeddings

5. **Ranking**

   * Combine candidate results
   * Score assessments using catalog metadata and semantic relevance
   * Select the top recommendations

6. **Catalog Validation**

   * Verify assessment names
   * Verify official SHL URLs
   * Remove invalid or hallucinated results

7. **Response Generation**

   * Generate a conversational reply
   * Return validated recommendations
   * Indicate whether additional clarification is required

---

### System Architecture

```text
    
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


```

### Design Principles

The system was designed around the following principles:

* **Modular Architecture** – Each component has a single responsibility.
* **Grounded Recommendations** – All assessments originate from the official SHL catalog.
* **Stateless API** – Conversation history is supplied with every request.
* **Explainable Retrieval** – Recommendations are based on structured retrieval rather than LLM-generated guesses.
* **Extensibility** – New retrieval strategies, ranking methods, or validation rules can be added without changing the API.

```

```rust
## 3. Retrieval Strategy

The quality of the recommendations depends on how effectively the system retrieves relevant assessments from the SHL catalog. Instead of relying solely on a Large Language Model (LLM), the system adopts a **hybrid retrieval pipeline** that combines structured keyword matching with semantic search. This approach improves recommendation accuracy while ensuring that every returned assessment exists in the official SHL catalog.

### Retrieval Objectives

The retrieval pipeline is designed to:

* Recommend only assessments from the official SHL catalog.
* Understand natural language hiring requirements.
* Support both exact keyword matching and semantic similarity.
* Rank assessments based on relevance and user constraints.
* Prevent hallucinated assessment names and invalid URLs.

---

### Hybrid Retrieval Pipeline

The recommendation workflow consists of the following stages:

#### 1. Query Context Extraction

The conversation history is analyzed to extract structured hiring requirements such as:

* Job role
* Technical skills
* Seniority level
* Assessment type
* Preferred language
* Assessment duration
* Remote or adaptive preferences
* Additional hiring constraints

Transforming conversational input into structured attributes enables more accurate retrieval than relying solely on free-text search.

---

#### 2. Keyword Retrieval

The first retrieval stage performs an exact search over the processed SHL catalog using catalog metadata.

This includes matching:

* Assessment names
* Job roles
* Skills
* Competencies
* Assessment categories
* Languages
* Other structured catalog fields

Keyword retrieval provides high precision whenever the user's wording closely matches the catalog.

---

#### 3. Semantic Retrieval

In parallel, the system performs semantic search over the vector index.

Unlike keyword matching, semantic retrieval can identify relevant assessments even when the user's wording differs from the catalog.

Examples include:

* Synonyms
* Similar job titles
* Related competencies
* Equivalent hiring requirements

This improves recall while maintaining recommendation quality.

---

#### 4. Candidate Merging

Results from both retrieval methods are merged into a single candidate pool.

During this stage:

* Duplicate assessments are removed.
* Scores from different retrieval methods are combined.
* All candidate assessments move to the ranking stage.

---

#### 5. Ranking Engine

Candidate assessments are ranked using multiple relevance signals instead of retrieval score alone.

Ranking considers factors such as:

* Semantic similarity
* Keyword relevance
* Job level compatibility
* Assessment category
* Language availability
* Assessment duration
* Remote or adaptive support
* User preferences collected during the conversation

This produces a shortlist that best matches the hiring requirements.

---

#### 6. Catalog Validation

Before recommendations are returned, every assessment is validated against the processed SHL catalog.

The validation process verifies:

* Assessment name
* Official SHL URL
* Assessment availability

Any invalid or hallucinated recommendation is discarded before generating the final response.

---

### Retrieval Workflow

```text
                 Conversation History
                          │
                          ▼
              Query Context Extraction
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
 Keyword-Based Retrieval          Semantic Retrieval
        │                                   │
        └─────────────────┬─────────────────┘
                          ▼
                 Candidate Merging
                          │
                          ▼
                  Multi-factor Ranking
                          │
                          ▼
                 Catalog Validation
                          │
                          ▼
              Top 1–10 Recommendations
```

---

### Why Hybrid Retrieval?

A keyword-only approach performs well for exact catalog matches but struggles with paraphrased or incomplete user queries. Conversely, relying solely on semantic search may retrieve conceptually similar assessments while missing important catalog-specific details.

By combining both techniques, the system benefits from:

* **High Precision** through keyword retrieval.
* **High Recall** through semantic search.
* **Grounded Recommendations** through catalog validation.
* **Reliable Ranking** using both semantic relevance and structured catalog metadata.

This hybrid strategy enables the assistant to produce accurate, explainable, and trustworthy assessment recommendations while remaining fully grounded in the official SHL catalog.

```

```rust
## 4. Conversation Management

The assistant is designed to support natural, multi-turn conversations while maintaining a **stateless API architecture**. Instead of storing session data on the server, every request includes the complete conversation history, allowing the agent to reconstruct the context before generating a response.

### Conversation Objectives

The conversation manager is responsible for:

* Understanding the user's intent.
* Maintaining context across multiple turns.
* Asking clarification questions when information is incomplete.
* Updating recommendations when requirements change.
* Comparing assessments using grounded catalog information.
* Ensuring responses remain relevant throughout the conversation.

---

### Conversation Workflow

Every conversation follows a structured decision-making process.

#### 1. Context Reconstruction

The complete conversation history is analyzed to build the current hiring context.

The reconstructed context may include:

* Job role
* Required skills
* Seniority level
* Assessment preferences
* Previous clarification answers
* User constraints
* Earlier recommendations

Since the API is stateless, this reconstruction occurs for every request.

---

#### 2. Intent Detection

The latest user message is classified into one of the supported conversation intents.

Supported intents include:

* New assessment recommendation
* Clarification response
* Recommendation refinement
* Assessment comparison
* General SHL-related question
* Unsupported or off-topic request

Identifying the correct intent ensures that the appropriate processing pipeline is executed.

---

#### 3. Clarification Strategy

Before generating recommendations, the system verifies whether sufficient information has been provided.

If important hiring details are missing, the assistant asks targeted follow-up questions instead of making assumptions.

Typical clarification topics include:

* Target job role
* Required technical skills
* Seniority level
* Assessment duration
* Personality or cognitive assessment preferences
* Language requirements

Once enough information is collected, the recommendation pipeline is executed.

---

#### 4. Recommendation Refinement

Users can modify their hiring requirements at any point during the conversation.

Examples include:

* Adding personality assessments
* Changing the target role
* Adjusting assessment duration
* Including additional technical skills
* Requesting adaptive or remote-friendly assessments

Instead of restarting the conversation, the assistant reconstructs the updated context and generates a revised shortlist.

---

#### 5. Assessment Comparison

The assistant also supports comparison requests between multiple SHL assessments.

During comparison, the system retrieves catalog information for each assessment and compares attributes such as:

* Assessment purpose
* Skills measured
* Target job level
* Duration
* Languages
* Assessment type

All comparison information is generated exclusively from the SHL catalog.

---

### Conversation Flow

```text 
            Conversation History
                     │
                     ▼
          Context Reconstruction
                     │
                     ▼
             Intent Detection
                     │
     ┌───────────────┼────────────────┐
     ▼               ▼                ▼
Clarification   Recommendation   Comparison
     │               │                │
     └───────────────┼────────────────┘
                     ▼
         Grounded Response Generation
                     │
                     ▼
              JSON API Response
```

---

### Design Principles

The conversation manager follows several key principles:

* **Context-Aware** – Uses the full conversation history to understand user requirements.
* **Clarification-First** – Requests missing information before generating recommendations.
* **Adaptive** – Updates recommendations whenever requirements change.
* **Grounded** – Generates responses using validated SHL catalog information.
* **Stateless** – Eliminates server-side session management while preserving conversational continuity.

This design enables the assistant to provide natural, flexible, and reliable interactions while ensuring that every recommendation remains accurate and fully grounded in the official SHL assessment catalog.

```

```rust
## 5. Evaluation Strategy

To ensure the reliability of the conversational recommendation system, the implementation was evaluated at both the **API level** and the **conversation level**. The objective was to verify not only the correctness of individual components but also the consistency of the end-to-end recommendation workflow.

### Evaluation Objectives

The evaluation focused on verifying that the system:

* Produces grounded SHL assessment recommendations.
* Correctly handles multi-turn conversations.
* Asks clarification questions when required.
* Updates recommendations as user requirements evolve.
* Rejects unsupported or out-of-scope requests.
* Returns responses that conform to the required API schema.

---

### API Testing

The FastAPI service was tested to verify endpoint functionality and response correctness.

| Component       | Validation                            |
| --------------- | ------------------------------------- |
| `/health`       | Service availability                  |
| `/chat`         | Response generation                   |
| Response Schema | Correct JSON structure                |
| Error Handling  | Graceful handling of invalid requests |

---

### Conversational Testing

Multiple conversation scenarios were evaluated to ensure that the agent behaved consistently across different interaction patterns.

Test scenarios included:

* Vague hiring requests requiring clarification
* Detailed job descriptions
* Multi-turn conversations
* Mid-conversation requirement changes
* Assessment comparison requests
* Off-topic questions
* Prompt injection attempts

These scenarios verified that the assistant maintained context correctly while producing grounded recommendations.

---

### Recommendation Validation

Every recommendation returned by the system is validated before being included in the final response.

The validation process checks:

* Assessment exists in the SHL catalog.
* Official SHL URL is returned.
* Duplicate recommendations are removed.
* Recommendation count remains within the required limit (1–10).

This additional validation layer prevents hallucinated assessment names and improves the trustworthiness of the system.

---

### Evaluation Summary

The evaluation demonstrates that the system is able to:

* Understand conversational hiring requirements.
* Ask meaningful clarification questions.
* Generate relevant SHL assessment recommendations.
* Update recommendations dynamically.
* Compare multiple assessments using grounded catalog information.
* Maintain compliance with the required stateless API specification.

Overall, the combination of modular testing, conversational evaluation, and catalog validation provides confidence that the recommendation pipeline behaves reliably across a variety of hiring scenarios.

```

```rust
## 6. Challenges, Trade-offs & Future Improvements

Designing a conversational recommendation system involves balancing natural language understanding with reliable and explainable recommendations. Throughout development, several architectural decisions were made to prioritize robustness, maintainability, and grounded responses.

### Challenges

#### Balancing Conversational Flexibility with Reliability

Large Language Models are effective at understanding user intent, but relying solely on an LLM can lead to hallucinated assessment names or unsupported recommendations.

To address this, the LLM is used only for:

* Understanding user intent
* Managing conversations
* Generating natural language responses

Assessment retrieval and validation are handled exclusively through the processed SHL catalog.

---

#### Handling Incomplete Requirements

Recruiters often begin with incomplete hiring requirements.

Instead of making assumptions, the assistant follows a **clarification-first** strategy by requesting missing information before generating recommendations.

This improves both recommendation quality and user experience.

---

#### Stateless Conversation Management

Maintaining conversational context without server-side sessions was another design challenge.

Using the complete conversation history in every request enables the assistant to reconstruct context while keeping the API stateless, scalable, and deployment-friendly.

---

### Design Trade-offs

Several trade-offs were made to keep the implementation simple and reliable.

| Decision             | Benefit                          | Trade-off                               |
| -------------------- | -------------------------------- | --------------------------------------- |
| Stateless API        | Easy to scale and deploy         | Slightly larger request payloads        |
| Hybrid Retrieval     | Improved recommendation accuracy | Additional retrieval complexity         |
| Catalog Validation   | Prevents hallucinations          | Extra validation step before responding |
| Modular Architecture | Easier maintenance and testing   | More components to coordinate           |

---

### Future Improvements

Several enhancements could further improve the recommendation system.

#### Retrieval Improvements

* Stronger embedding models
* Dedicated reranking models
* Learning-to-rank approaches
* Query expansion techniques

#### Conversation Improvements

* Personalized recommendations based on user feedback
* Smarter clarification question generation
* Better intent classification
* Support for longer conversations

#### Evaluation Improvements

* Larger benchmark datasets
* Automated conversation evaluation
* Offline retrieval metrics
* User feedback-based quality measurement

#### System Enhancements

* Caching frequently retrieved assessments
* Streaming responses
* Multi-language recommendation support
* Analytics dashboard for recommendation quality

---

### Final Remarks

The primary objective of this project was to build a conversational SHL assessment recommender that is **accurate, explainable, and grounded**. By combining conversational understanding with hybrid retrieval, catalog validation, and a modular architecture, the system satisfies the assignment requirements while remaining extensible for future enhancements.

The overall design emphasizes reliability over complexity, ensuring that every recommendation is both conversationally relevant and backed by official SHL catalog data.

```