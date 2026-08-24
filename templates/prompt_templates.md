# Prompt templates

This file contains example prompt templates for Stage A (compact review) and Stage B (expand per-shot voiceover and edit notes).

Stage A: compact review (use sparingly — only thumbnails + short excerpts)
- Provide EDL JSON with actions keep/cut/blur and a short reshoot checklist.

Stage B: expansion
- Given the accepted EDL, return a full voiceover script per shot, suggested on-screen callouts, and exact trim amounts.

Store these templates in scripts/summarize_llm.py and call your provider wrapper.
