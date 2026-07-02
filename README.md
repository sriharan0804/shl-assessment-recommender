```rust
---
title: SHL Assessment Recommender
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---
```

```rust
# SHL Conversational Assessment Recommender

A FastAPI-based conversational AI assistant that recommends the most suitable **SHL Individual Test Solutions** through natural language conversations. The system understands hiring requirements, asks clarification questions when needed, and returns grounded recommendations using the official SHL product catalog.

## Features

* Conversational assessment recommendations
* Clarification-first workflow for incomplete requirements
* Hybrid retrieval (Keyword + Semantic Search)
* Grounded recommendations from the official SHL catalog
* Dynamic recommendation refinement during conversation
* SHL assessment comparison
* Prompt injection and off-topic request guardrails
* Stateless REST API
* Catalog validation to prevent hallucinated recommendations

## Tech Stack

* **Backend:** FastAPI
* **Language:** Python 3.11+
* **LLM:** Google Gemini
* **Retrieval:** Hybrid (Keyword + Semantic Search)
* **Environment Management:** python-dotenv

## Project Structure

```text
.
├── app/
├── data/
├── tests/
├── requirements.txt
├── .env.example
├── README.md
└── approach.md
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Endpoints

| Endpoint      | Description                                   |
| ------------- | --------------------------------------------- |
| `GET /health` | Health check endpoint                         |
| `POST /chat`  | Conversational SHL assessment recommendations |

## Documentation

After starting the server, open:

* `http://127.0.0.1:8000/docs` – Swagger UI
* `http://127.0.0.1:8000/redoc` – ReDoc documentation

## Design Highlights

* Stateless conversation management
* Hybrid retrieval pipeline
* Catalog-grounded recommendations
* Modular architecture
* Explainable recommendation workflow

## License

This project was developed as part of the SHL Conversational Assessment Recommender assessment.

```