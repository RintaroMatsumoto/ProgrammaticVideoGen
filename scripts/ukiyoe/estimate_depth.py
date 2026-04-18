#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Estimate a depth map for a ukiyoe image using Depth Anything V2.

Optional / Phase 2. MVP does not require this step.

Usage:
    python scripts/ukiyoe/estimate_depth.py kanagawa_wave
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--model", default="depth-anything/Depth-Anything-V2-Large-hf")
    args = parser.parse_args()

    try:
        from transformers import pipeline
        import torch
    except ImportError:
        print("[error] pip install torch transformers accelerate")
        return 2

    repo = Path(__file__).resolve().parent.parent.parent
    img_dir = repo / "public" / "ukiyoe" / args.name
    original = next((p for p in img_dir.glob("original.*")
                     if p.suffix.lower() in (".jpg", ".jpeg", ".png")), None)
    if not original:
        print(f"[error] original not found in {img_dir}")
        return 1

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[depth] loading {args.model} on {device}")
    pipe = pipeline("depth-estimation", model=args.model, device=device)

    pil = Image.open(original).convert("RGB")
    print(f"[depth] processing {pil.size}")
    result = pipe(pil)

    depth = result["depth"]  # PIL.Image, mode 'I' or similar
    arr = np.array(depth).astype(np.float32)
    arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    arr = (arr * 255).astype(np.uint8)
    depth_png = Image.fromarray(arr, mode="L")

    out_path = img_dir / "depth.png"
    depth_png.save(out_path)
    print(f"[ok] depth map: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
