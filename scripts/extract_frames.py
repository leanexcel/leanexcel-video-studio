"""extract_frames.py

Extract thumbnails from a video every N seconds using ffmpeg.
Requires ffmpeg to be installed and available on PATH.
"""
import argparse
import os
import subprocess

def extract_frames(video_path, out_dir, interval=3):
    os.makedirs(out_dir, exist_ok=True)
    # ffmpeg command: select frames every N seconds
    # -vf fps=1/INTERVAL will extract 1 frame per INTERVAL seconds
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        os.path.join(out_dir, "thumb%04d.jpg")
    ]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="Path to input video (mp4)")
    parser.add_argument("out_dir", help="Directory to save thumbnails")
    parser.add_argument("--interval", type=int, default=3, help="Seconds between thumbnails")
    args = parser.parse_args()
    extract_frames(args.video, args.out_dir, args.interval)
