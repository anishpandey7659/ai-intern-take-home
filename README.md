# AI Intern — Pre-Hiring Take-Home Assignment

A Python-based assignment covering data cleaning, basic NLP preprocessing, REST API integration, error handling, and fundamental concepts of LLMs, RAG, and AI safety.

## Project Overview

This project implements two Python modules and a written case study:

- **Part 1 – Data Cleaning & NLP:** Cleans noisy helpdesk tickets, removes duplicates and invalid records, preprocesses text, and generates keyword statistics.
- **Part 2 – API Integration:** Fetches sample posts from JSONPlaceholder, transforms the responses into structured documents, and handles network failures with fallback data.
- **Part 3 – AI, RAG & Safety:** Explores prompt engineering, hallucination prevention, document chunking, and prompt injection defense.

## Project Structure

```text
AI-Intern-Assignment/
│
├── data/
│   ├── support_tickets.json
│   └── cleaned_tickets.json
│
├── src/
│   ├── task1_nlp_cleaner.py
│   └── task2_api_client.py
│
├── ANSWERS.md
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10+
- pip
- Git

## Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/anishpandey7659/ai-intern-take-home.git
cd ai-intern-take-home
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the virtual environment**

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

## Running the Project

**Part 1: Data Cleaning & NLP**

```bash
python src/task1_nlp_cleaner.py
```

This script:
- Removes duplicate tickets using `ticket_id`.
- Filters invalid and empty queries.
- Removes HTML tags and unnecessary whitespace.
- Converts text to lowercase and removes punctuation.
- Tokenizes text and removes common English stop words.
- Generates category statistics and the top 5 frequent keywords.
- Saves the processed records to `data/cleaned_tickets.json`.

**Part 2: API Integration**

```bash
python src/task2_api_client.py
```

This script:
- Sends a GET request to the JSONPlaceholder API.
- Retrieves and transforms the first five posts.
- Calculates word counts for each document.
- Handles HTTP errors, connection errors, and timeouts.
- Provides fallback mock documents if the API request fails.

**Part 3: Written Case Study**

Refer to [ANSWERS.md](ANSWERS.md) for explanations and solutions covering:

- Prompt engineering and hallucination control.
- Temperature and Top-p.
- RAG document chunking and overlap.
- Prompt injection attacks and defensive guardrails.

## Assumptions & Design Decisions

- Duplicate tickets are identified using `ticket_id`, retaining the first occurrence.
- Tickets with missing, empty, or whitespace-only queries are considered invalid.
- A predefined English stop-word list is used for basic NLP preprocessing.
- The API integration uses JSONPlaceholder as a public sample REST API.
- Mock documents are used as a fallback when the API is unavailable.
- No paid LLM API or external AI service is required.

## Error Handling

The API client uses Python's `logging` module to record request progress and failures. Network timeouts, connection errors, and HTTP errors are handled gracefully to prevent unexpected application crashes.

## Dependencies

See [requirements.txt](requirements.txt) for the complete list of project dependencies.

## Author

**Anish Pandey**

AI / ML Enthusiast | Python Developer

