"""Fetch and normalize sample articles from JSONPlaceholder."""

import json
import logging
from typing import Any
import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL")
if not API_URL:
    raise ValueError("API_URL environment variable is required")

REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT") or "30")

logger = logging.getLogger(__name__)


def fetch_posts(
    url: str = API_URL,
    timeout: float = REQUEST_TIMEOUT,
) -> list[object]:
    """Fetch at most five posts, validating the response shape."""
    logger.info("Starting request to %s", url)
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    try:
        payload = response.json()
    except (requests.exceptions.JSONDecodeError, json.JSONDecodeError) as error:
        raise ValueError("The API response was not valid JSON") from error

    if not isinstance(payload, list):
        raise ValueError("Expected the API response to be a list of posts")

    posts = payload[:5]
    logger.info(
        "Request succeeded with HTTP %s; received %d posts",
        response.status_code,
        len(posts),
    )
    return posts


def transform_posts(posts: list[object]) -> list[dict[str, Any]]:
    """Convert API posts to normalized document records."""
    documents: list[dict[str, Any]] = []

    for post in posts:
        if not isinstance(post, dict):
            logger.warning("Skipping invalid post")
            continue

        documents.append(
            {
                "doc_id": post["id"],
                "title": post["title"].strip(),
                "content": post["body"].replace("\n", " ").strip(),
                "word_count": len(post["body"].split()),
            }
        )

    return documents


def fallback_documents() -> list[dict[str, Any]]:
    """Return two mock documents if the API request fails."""
    return [
        {
            "doc_id": "fallback-1",
            "title": "Helpdesk Support Guide",
            "content": "Contact the helpdesk for technical support.",
            "word_count": 7,
        },
        {
            "doc_id": "fallback-2",
            "title": "Remote Work Policy",
            "content": "Employees should follow their team's remote work schedule.",
            "word_count": 9,
        },
    ]


def get_documents(
    url: str = API_URL,
    timeout: float = REQUEST_TIMEOUT,
) -> list[dict[str, Any]]:
    """Fetch and transform documents, using fallback records on request failure."""
    try:
        documents = transform_posts(fetch_posts(url=url, timeout=timeout))
        if not documents:
            raise ValueError("The API response contained no usable posts")
    except requests.exceptions.Timeout:
        logger.error("Request to %s timed out", url)
        logger.warning("Using two fallback documents")
        return fallback_documents()
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to %s", url)
        logger.warning("Using two fallback documents")
        return fallback_documents()
    except requests.exceptions.HTTPError as error:
        logger.error("API returned an unsuccessful HTTP status: %s", error)
        logger.warning("Using two fallback documents")
        return fallback_documents()
    except requests.exceptions.RequestException as error:
        logger.error("Request to %s failed: %s", url, error)
        logger.warning("Using two fallback documents")
        return fallback_documents()
    except ValueError as error:
        logger.error("Unexpected API response: %s", error)
        logger.warning("Using two fallback documents")
        return fallback_documents()

    logger.info("Returning %d transformed documents", len(documents))
    return documents


def main() -> None:
    """Fetch articles and print them as JSON."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print(json.dumps(get_documents(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
