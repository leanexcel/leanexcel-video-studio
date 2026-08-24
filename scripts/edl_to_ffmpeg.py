"""edl_to_ffmpeg.py

Apply a simple EDL (JSON format) to trim and concatenate video segments using ffmpeg.
EDL format (JSON array of segments):
[
  {"id": 1, "start_sec": 0.0, "end_sec": 10.0, "action": "keep", "note": "Intro"},
  ...
]
"""
import json
import subprocess
import os


def apply_edl(video_path, edl_json, out_path):
    with open(edl_json, 'r', encoding='utf-8') as f:
        edl = json.load(f)
    os.makedirs('edl_tmp', exist_ok=True)
    parts = []
    for seg in edl:
        if seg.get('action') != 'keep':
            continue
        start = seg['start_sec']
        duration = seg['end_sec'] - seg['start_sec']
        out_seg = f"edl_tmp/part_{seg['id']:03d}.mp4"
        cmd = [
            'ffmpeg', '-y', '-i', video_path,
            '-ss', str(start), '-t', str(duration),
            '-c', 'copy', out_seg
        ]
        subprocess.run(cmd, check=True)
        parts.append(out_seg)
    if not parts:
        raise RuntimeError('No parts to concatenate')
    concat_file = 'edl_tmp/parts.txt'
    with open(concat_file, 'w', encoding='utf-8') as fh:
        for p in parts:
            fh.write(f"file '{os.path.abspath(p)}'\n")
    cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', out_path]
    subprocess.run(cmd, check=True)
    print(f"Draft video produced at {out_path}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('video')
    parser.add_argument('edl_json')
    parser.add_argument('out')
    args = parser.parse_args()
    apply_edl(args.video, args.edl_json, args.out)
