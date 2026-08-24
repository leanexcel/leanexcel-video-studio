import os
import openai

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise RuntimeError('OpenAI API key not found in OPENAI_API_KEY environment variable')
openai.api_key = OPENAI_API_KEY


def chat_completion(messages, model='gpt-4', temperature=0.2, max_tokens=1500):
    """Call OpenAI Chat Completions and return the assistant text.

    messages: list of dicts {role: 'system'|'user'|'assistant', 'content': str}
    """
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content
