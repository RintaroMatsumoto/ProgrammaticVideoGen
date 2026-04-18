#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inpaint hidden areas behind foreground layers using FLUX.1 (or SD inpaint).

Optional / Phase 2. MVPは呼ばない。

入力:  public/ukiyoe/<name>/layers/*.png （SAM2出力）
出力:  public/ukiyoe/<name>/layers/<layer>_filled.png
       （手前レイヤーで隠れていた奥の領域を浮世絵風に補完）

Notes:
- FLUX.1-schnell (Apache 2.0) を HuggingFace diffusers 経由で利用。
- 浮世絵アニメ化では、手前の被写体を抜いた後、その穴を埋めないと
  パララックス時に背景に黒い抜けが発生する。
- 厳密な完成度は要らない。パララックスで一瞬見える程度。
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
    parser.add_argument("--model", default="black-forest-labs/FLUX.1-schnell")
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--prompt",
                        default="Japanese ukiyo-e woodblock print, flat colors, "
                                "visible paper texture, traditional Hokusai style, "
                                "same background continuation")
    args = parser.parse_args()

    try:
        import torch
        from diffusers import FluxInpaintPipeline
    except ImportError:
        print("[error] pip install torch diffusers accelerate transformers")
        return 2

    repo = Path(__file__).resolve().parent.parent.parent
    img_dir = repo / "public" / "ukiyoe" / args.name
    layers_dir = img_dir / "layers"
    if not layers_dir.exists():
        print(f"[error] layers dir not found: {layers_dir}")
        print("Run segment_layers.py first.")
        return 1

    original = next((p for p in img_dir.glob("original.*")
                     if p.suffix.lower() in (".jpg", ".jpeg", ".png")), None)
    if not original:
        print(f"[error] original not found in {img_dir}")
        return 1

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    print(f"[flux] loading {args.model} on {device}")
    pipe = FluxInpaintPipeline.from_pretrained(args.model, torch_dtype=dtype)
    pipe.to(device)

    base = Image.open(original).convert("RGB")
    w, h = base.size

    # 各レイヤーについて、そのレイヤーのアルファ=不透明部分を
    # 「埋めるべき領域」として指定し、奥の背景を推定補完する。
    for layer_path in sorted(layers_dir.glob("*.png")):
        if layer_path.name.endswith("_filled.png"):
            continue
        layer = Image.open(layer_path).convert("RGBA")
        alpha = np.array(layer.split()[3])
        mask = (alpha > 32).astype(np.uint8) * 255
        mask_img = Image.fromarray(mask, mode="L")

        out_path = layers_dir / f"{layer_path.stem}_filled.png"
        if out_path.exists():
            print(f"[skip] {out_path.name}")
            continue
        print(f"[flux] inpaint {layer_path.name} ({w}x{h}, steps={args.steps})")
        result = pipe(
            prompt=args.prompt,
            image=base,
            mask_image=mask_img,
            num_inference_steps=args.steps,
            guidance_scale=0.0,
            width=w,
            height=h,
        ).images[0]
        result.save(out_path, "PNG")
        print(f"       → {out_path}")

    print("[ok] inpainting complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
