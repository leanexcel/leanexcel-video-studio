"""planner.py

Convert a short outline or title into a structured shotlist template.
This is a minimal starter script that creates a JSON shotlist from a short outline.
"""
import json
import sys

TEMPLATE = {
    "shots": []
}

def outline_to_shotlist(title, outline_lines):
    shots = []
    for i, line in enumerate(outline_lines, start=1):
        shots.append({
            "id": i,
            "title": line.strip(),
            "expected_duration_sec": 10,
            "notes": "Describe what to show on-screen and the key voiceover bullets",
        })
    return {"video_title": title, "shots": shots}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python scripts/planner.py \"Video Title\" \"line1;line2;line3\"")
        sys.exit(1)
    title = sys.argv[1]
    lines = sys.argv[2].split(";")
    shotlist = outline_to_shotlist(title, lines)
    print(json.dumps(shotlist, indent=2))
