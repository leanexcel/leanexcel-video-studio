# Workflow

This repo contains an automated pipeline for planning, analyzing, and producing draft edits for screen-recorded videos.

High-level steps:
1. Pre-production planner: convert an outline into an ordered shotlist.
2. Guided recording (optional): teleprompter/hotkey sidecar to embed markers while recording in Camtasia.
3. Ingest: export MP4 from Camtasia and import the sidecar markers.
4. Fast analysis: extract thumbnails, run OCR, and transcribe audio with Whisper.
5. LLM-driven review: generate an Edit Decision List (EDL) and per-shot voiceover suggestions.
6. Edit automation: apply EDL via ffmpeg and generate draft video.
7. TTS: generate per-shot voiceovers with ElevenLabs (or local TTS) and align.

See docs/ for more details and usage examples.
