"""ocr_analysis.py

Run Tesseract OCR on thumbnails and save results.
Requires Tesseract to be installed and pytesseract available.
"""
import os
import json
import glob
from PIL import Image
import pytesseract


def ocr_on_folder(thumbs_dir, out_json):
    results = []
    files = sorted(glob.glob(os.path.join(thumbs_dir, '*.jpg')))
    for f in files:
        img = Image.open(f)
        text = pytesseract.image_to_string(img)
        results.append({"file": os.path.basename(f), "text": text})
    with open(out_json, 'w', encoding='utf-8') as fh:
        json.dump(results, fh, ensure_ascii=False, indent=2)
    print(f"OCR results saved to {out_json}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('thumbs_dir')
    parser.add_argument('out_json')
    args = parser.parse_args()
    ocr_on_folder(args.thumbs_dir, args.out_json)
