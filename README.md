```rust
# SHL Assessment Recommender

A FastAPI-based conversational agent that recommends SHL Individual Test Solutions based on hiring needs.

## Features

- Clarifies vague hiring requests
- Recommends 1–10 SHL assessments
- Uses catalog-only recommendations
- Supports refinement during conversation
- Supports assessment comparison
- Refuses off-topic and prompt-injection requests
- Provides stateless `/chat` API

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```