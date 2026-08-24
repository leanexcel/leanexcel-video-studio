"""transcribe.py

Wrapper to run Whisper locally (if installed) or call OpenAI Whisper API.
This script provides a simple interface and saves a JSON transcription.
"""
import argparse
import json
import os

try:
    import whisper
except Exception:
    whisper = None


def transcribe_local(video_path, model_name="small"):
    if whisper is None:
        raise RuntimeError("whisper not available; pip install -U openai-whisper or use API")
    model = whisper.load_model(model_name)
    result = model.transcribe(video_path)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="Path to input video (mp4)")
    parser.add_argument("--model", default="small")
    parser.add_argument("--out", default="transcript.json")
    args = parser.parse_args()
    res = transcribe_local(args.video, args.model)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"Transcription saved to {args.out}")
