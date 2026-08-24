"""summarize_llm.py

Provider-agnostic adapter for Stage A summarization prompt.
This file contains prompt templates and a simple function that formats a compact payload.
Implement the provider call in your environment (OpenAI, Cursor, etc.).
"""
import json

STAGE_A_PROMPT = """
You are a video reviewer. Given the following compact summary of a recorded video (title, a few thumbnails filenames and OCR/text snippets, marker timestamps, and short transcript excerpts), provide:
1) Up to 5 top problems (missing steps, privacy issues, confusing order) with short explanations.
2) A prioritized re-shoot checklist (if needed), detailing which shots to re-record and in what order.
3) A suggested Edit Decision List (EDL) as JSON array with fields: id, start_sec, end_sec, action (keep/cut/blur), and short note.

CompactSummary:
{compact_summary}

Return only valid JSON for the EDL and the lists.
"""


def build_stage_a_prompt(compact_summary):
    return STAGE_A_PROMPT.format(compact_summary=json.dumps(compact_summary, indent=2))

if __name__ == '__main__':
    import sys
    example = {"title": "Example", "thumbnails": ["thumb0001.jpg"], "ocr": [], "markers": [], "transcript_excerpts": []}
    prompt = build_stage_a_prompt(example)
    print(prompt)
