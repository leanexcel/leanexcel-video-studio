"""OpenAI adapter used by the video pipeline.

Requires the modern OpenAI Python SDK (>=1.0).
The API key is read from OPENAI_API_KEY; it is never stored in the repo.
"""
import os

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def chat_completion(messages, model=None, temperature=0.2, max_tokens=1500):
    """Call OpenAI Chat Completions and return the assistant text.

    ``messages`` is a list of dictionaries with ``role`` and ``content``.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OpenAI API key not found. Set the OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model or DEFAULT_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    if not response.choices or not response.choices[0].message:
        raise RuntimeError("OpenAI returned an empty completion.")

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("OpenAI returned no message content.")
    return content
