import json
import re
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any


_HTML_TAG_PATTERN = re.compile(r"<[^>]*>")
_WHITESPACE_PATTERN = re.compile(r"\s+")
_NON_WORD_PATTERN = re.compile(r"[^\w]+|_+", flags=re.UNICODE)
_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "do",
    "for", "from", "how", "i", "in", "is", "it", "my", "of", "on", "or",
    "the", "to", "was", "what", "when", "where", "which", "who", "why",
    "after",
    "with",
}

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_INPUT_PATH = _PROJECT_ROOT / "data" / "support_tickets.json"
_OUTPUT_PATH = _PROJECT_ROOT / "data" / "cleaned_tickets.json"

def clean_tickets(tickets: Iterable[object]) -> list[dict[str, Any]]:
    """Return cleaned ticket copies, keeping only the first record per ticket ID."""
    cleaned: list[dict[str, Any]] = []
    seen_ticket_ids: set[object] = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            continue

        ticket_id = ticket.get("ticket_id")
        if ticket_id is None:
            continue

        # Check wheather the ticket_id is hashable; if not, skip this ticket,cause set can only contain hashable objects.
        try:
            hash(ticket_id)
        except TypeError:
            continue

        if ticket_id in seen_ticket_ids:
            continue
        seen_ticket_ids.add(ticket_id)

        query = ticket.get("query")
        if not isinstance(query, str) or not query.strip():
            continue

        # Removing HTML tags and extra whitespace, then stripping leading/trailing whitespace.
        query = _HTML_TAG_PATTERN.sub(" ", query)
        query = _WHITESPACE_PATTERN.sub(" ", query).strip()
        if not query:
            continue

        cleaned_ticket = ticket.copy()
        cleaned_ticket["query"] = query
        cleaned.append(cleaned_ticket)

    return cleaned


def preprocess_text(text: str) -> list[str]:
    """Lowercase, tokenize on non-alphanumeric characters, and remove stop words."""
    normalized = _NON_WORD_PATTERN.sub(" ", text.lower())
    return [
        token
        for token in normalized.split()
        if token not in _STOP_WORDS
    ]


def analyze_tickets(
    cleaned_tickets: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Add query tokens, print category and keyword counts, and save the records."""
    tokenized_tickets: list[dict[str, Any]] = []
    category_counts: Counter[str] = Counter()
    keyword_counts: Counter[str] = Counter()

    for ticket in cleaned_tickets:

        # Tokenize the query and update counts for keywords and categories.
        tokenized_ticket = ticket.copy()
        tokens = preprocess_text(ticket["query"])
        tokenized_ticket["tokens"] = tokens
        tokenized_tickets.append(tokenized_ticket)
        keyword_counts.update(tokens)

        category = ticket.get("category")
        if isinstance(category, str):
            category_counts[category] += 1

    # Sort the keywords by frequency (descending) and alphabetically for ties, then take the top 5.
    top_keywords = sorted(
        keyword_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )[:5]

    print(f"Tickets by category: {dict(sorted(category_counts.items()))}")
    print(f"Top 5 keywords: {top_keywords}")

    _OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _OUTPUT_PATH.write_text(
        json.dumps(tokenized_tickets, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return tokenized_tickets


def main() -> None:
    """Load, clean, analyze, and save the support tickets."""
    with _INPUT_PATH.open(encoding="utf-8") as input_file:
        tickets = json.load(input_file)

    if not isinstance(tickets, list):
        raise ValueError(f"Expected a list of tickets in {_INPUT_PATH}")

    # Clean the tickets and analyze them.
    cleaned_tickets = clean_tickets(tickets)
    analyze_tickets(cleaned_tickets)


if __name__ == "__main__":
    main()
