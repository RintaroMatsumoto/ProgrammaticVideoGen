#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Segment a ukiyoe image into semantic layers using Segment Anything Model v2 (SAM2).

Optional / Phase 2. The MVP pipeline runs without this step (uses Ken Burns only).
When run, outputs layer PNGs to public/ukiyoe/<name>/layers/*.png.

Setup:
    pip install torch transformers accelerate Pillow
    # SAM2: install per https://github.com/facebookresearch/sam2
    #   pip install "sam2 @ git+https://github.com/facebookresearch/sam2.git"

Usage:
    python scripts/ukiyoe/segment_layers.py kanagawa_wave \
        --points-file scripts/ukiyoe/prompts/kanagawa_wave.json

Prompt file format (per-layer point prompts):
    {
      "wave_main":  {"points": [[x, y]], "labels": [1]},
      "fuji":       {"points": [[x, y]], "labels": [1]},
      ...
    }
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')


def load_sam2():
    """Lazy import — only needed if this script is executed."""
    try:
        from sam2.sam2_image_predictor import SAM2ImagePredictor
        return SAM2ImagePredictor
    except ImportError:
        print("[error] SAM2 not installed.")
        print("Install: pip install 'sam2 @ git+https://github.com/facebookresearch/sam2.git'")
        sys.exit(2)


def extract_layer(image_rgba: np.ndarray, mask: np.ndarray) -> Image.Image:
    """Apply mask as alpha and return an RGBA PIL Image with transparent background."""
    h, w = image_rgba.shape[:2]
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., :3] = image_rgba[..., :3]
    out[..., 3] = (mask.astype(np.uint8) * 255)
    return Image.fromarray(out, mode="RGBA")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--points-file", type=Path, required=False,
                        help="JSON with per-layer point prompts")
    parser.add_argument("--model", default="facebook/sam2-hiera-large")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent.parent.parent
    img_dir = repo / "public" / "ukiyoe" / args.name
    original = next((p for p in img_dir.glob("original.*")
                     if p.suffix.lower() in (".jpg", ".jpeg", ".png")), None)
    if not original:
        print(f"[error] original image not found in {img_dir}")
        return 1

    if args.points_file is None:
        args.points_file = Path(__file__).parent / "prompts" / f"{args.name}.json"
    if not args.points_file.exists():
        print(f"[error] prompt file not found: {args.points_file}")
        print("Create a prompt file with per-layer point coordinates.")
        return 1
    prompts = json.loads(args.points_file.read_text(encoding="utf-8"))

    SAM2ImagePredictor = load_sam2()
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[sam2] loading {args.model} on {device}")
    predictor = SAM2ImagePredictor.from_pretrained(args.model)

    pil = Image.open(original).convert("RGB")
    image_np = np.array(pil)
    predictor.set_image(image_np)

    out_dir = img_dir / "layers"
    out_dir.mkdir(parents=True, exist_ok=True)

    image_rgba = np.dstack([image_np, np.full(image_np.shape[:2], 255, dtype=np.uint8)])

    for layer_name, prompt in prompts.items():
        points = np.array(prompt["points"], dtype=np.float32)
        labels = np.array(prompt.get("labels", [1] * len(points)), dtype=np.int32)
        print(f"[sam2] segmenting {layer_name} ...")
        masks, scores, _ = predictor.predict(
            point_coords=points, point_labels=labels, multimask_output=True
        )
        # pick best mask
        best = int(np.argmax(scores))
        mask = masks[best]
        layer_img = extract_layer(image_rgba, mask)
        out_path = out_dir / f"{layer_name}.png"
        layer_img.save(out_path, "PNG")
        print(f"       → {out_path}")

    print(f"[ok] {len(prompts)} layers written to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
