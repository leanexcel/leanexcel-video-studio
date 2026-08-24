"""stage_a.py

Run the Stage A compact review using OpenAI Chat to generate problems, a reshoot checklist, and an EDL.

Usage:
  python scripts/stage_a.py --video examples/sample.mp4 --thumbs artifacts/thumbs --ocr artifacts/ocr.json --transcript artifacts/transcript.json --out artifacts/stage_a_output.json

Requirements:
  - OPENAI_API_KEY in env
  - scripts/summarize_llm.py available

"""
import argparse
import json
import os
import glob
import re
from pathlib import Path

from scripts import summarize_llm
from scripts.llm_openai import chat_completion


def safe_read_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def extract_text_snippets_from_ocr(ocr_list, max_items=6):
    snippets = []
    for item in ocr_list[:max_items]:
        text = item.get('text','').strip()
        if text:
            # take first 200 chars
            snippets.append({'file': item.get('file'), 'text': text[:200]})
    return snippets


def transcript_excerpts(transcript_json, max_excerpts=3):
    excerpts = []
    if not transcript_json:
        return excerpts
    # Whisper local format has 'segments' list with start/end and text
    segments = transcript_json.get('segments') or []
    if not segments and isinstance(transcript_json.get('text'), str):
        excerpts.append({'text': transcript_json.get('text')[:300]})
        return excerpts
    # pick first, middle, last segments if available
    if segments:
        idxs = [0]
        if len(segments) > 2:
            idxs.append(len(segments)//2)
        if len(segments) > 1:
            idxs.append(len(segments)-1)
        for i in idxs[:max_excerpts]:
            seg = segments[i]
            excerpts.append({'start': seg.get('start'), 'end': seg.get('end'), 'text': seg.get('text')[:300]})
    return excerpts


def build_compact_summary(video_path, thumbs_dir, ocr_json, transcript_json, markers_json=None, max_thumbs=8):
    thumb_files = sorted(glob.glob(os.path.join(thumbs_dir, '*.jpg')))
    # limit thumbnails
    thumbs = [os.path.basename(p) for p in thumb_files[:max_thumbs]]
    ocr_list = safe_read_json(ocr_json) or []
    ocr_snips = extract_text_snippets_from_ocr(ocr_list, max_items=6)
    transcript = safe_read_json(transcript_json)
    excerpts = transcript_excerpts(transcript, max_excerpts=3)
    markers = safe_read_json(markers_json) if markers_json else []
    summary = {
        'video': os.path.basename(video_path) if video_path else None,
        'thumbnails': thumbs,
        'ocr_snippets': ocr_snips,
        'transcript_excerpts': excerpts,
        'markers': markers,
    }
    return summary


def extract_json_from_text(text):
    # find first JSON object or array in text
    json_regex = re.compile(r'(\{.*\}|\[.*\])', re.DOTALL)
    m = json_regex.search(text)
    if not m:
        return None
    jtext = m.group(1)
    try:
        return json.loads(jtext)
    except Exception:
        # try to fix common issues: replace single quotes with double quotes
        try:
            fixed = jtext.replace("'", '"')
            return json.loads(fixed)
        except Exception:
            return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', help='path to mp4', required=False)
    parser.add_argument('--thumbs', help='thumbnails directory', required=True)
    parser.add_argument('--ocr', help='ocr json', required=True)
    parser.add_argument('--transcript', help='transcript json (whisper)', required=False)
    parser.add_argument('--markers', help='optional markers json', required=False)
    parser.add_argument('--out', help='output json file', default='artifacts/stage_a_output.json')
    parser.add_argument('--model', help='OpenAI model for chat', default='gpt-4')
    args = parser.parse_args()

    compact = build_compact_summary(args.video, args.thumbs, args.ocr, args.transcript, args.markers)
    prompt = summarize_llm.build_stage_a_prompt(compact)

    system_msg = {"role": "system", "content": "You are a helpful assistant that inspects compact video summaries and returns a focused JSON output: problems, reshoot_checklist, and edl."}
    user_msg = {"role": "user", "content": prompt}

    print('Calling OpenAI Chat...')
    resp_text = chat_completion([system_msg, user_msg], model=args.model, temperature=0.1, max_tokens=1500)

    # Save raw response
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_file = Path(out_dir) / 'stage_a_raw.txt'
    raw_file.write_text(resp_text, encoding='utf-8')

    parsed = extract_json_from_text(resp_text)
    if parsed is None:
        print('Warning: Could not parse JSON from LLM response. Saved raw response to', raw_file)
        # Save minimal JSON wrapper with raw text
        result = {'success': False, 'raw': resp_text}
    else:
        result = {'success': True, 'parsed': parsed}
    # Also include compact summary for reference
    result['compact_summary'] = compact
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)
    print('Stage A output saved to', args.out)
