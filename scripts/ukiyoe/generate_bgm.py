#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
和風 BGM 合成器。

numpy だけで作る 4 分の静かなペンタトニック・ドローン。
- スケール: C ヨナ抜き風 (C, D, F, G, A)
- 3 つの和音パッドがゆっくりクロスフェードで遷移
- ステレオ微デチューンで幅を作る
- ナレーションの邪魔をしないよう低音域中心・高域控えめ

著作権フリー（自家生成なので当然 CC0）。
商用 OK、加工 OK、配布 OK。
"""
from __future__ import annotations

import argparse
import math
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

SR = 44100
PENTA_C = [261.63, 293.66, 349.23, 392.00, 440.00]  # C D F G A

# 3 つの和音進行（基音を変えて雰囲気を変える）
CHORDS = [
    [PENTA_C[0], PENTA_C[2], PENTA_C[4]],  # C F A
    [PENTA_C[1], PENTA_C[3], PENTA_C[4]],  # D G A
    [PENTA_C[0], PENTA_C[1], PENTA_C[3]],  # C D G
]


def pad_voice(freq: float, dur_s: float, detune: float = 0.0) -> np.ndarray:
    """ゆったり立ち上がる正弦+三角のパッド音。"""
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    f = freq * (1.0 + detune)
    # 基本波 + オクターブ下 + 5度上（やさしい倍音）
    s = (
        0.50 * np.sin(2 * np.pi * f * t)
        + 0.22 * np.sin(2 * np.pi * (f / 2) * t)
        + 0.14 * np.sin(2 * np.pi * (f * 1.5) * t)
    )
    # 三角波を少しブレンド（弦っぽさ）
    tri = 2.0 / np.pi * np.arcsin(np.sin(2 * np.pi * f * 0.5 * t))
    s = 0.80 * s + 0.12 * tri

    # 8 秒の立ち上がり、4 秒のリリース
    env = np.ones(n)
    atk = min(int(8 * SR), n // 3)
    rel = min(int(4 * SR), n // 4)
    env[:atk] = np.linspace(0, 1, atk) ** 2
    env[-rel:] = np.linspace(1, 0, rel) ** 2
    # 低周波ゆらぎ（呼吸感）
    breath = 1.0 + 0.08 * np.sin(2 * np.pi * 0.09 * t)
    return s * env * breath


def chord_block(freqs: list[float], dur_s: float) -> np.ndarray:
    """3 音のパッドを重ねた和音ブロック。ステレオで左右に微デチューン。"""
    left = np.zeros(int(dur_s * SR))
    right = np.zeros(int(dur_s * SR))
    for f in freqs:
        vL = pad_voice(f, dur_s, detune=-0.0025)
        vR = pad_voice(f, dur_s, detune=+0.0025)
        left += vL
        right += vR
    # 正規化
    peak = max(np.abs(left).max(), np.abs(right).max(), 1e-9)
    left /= peak
    right /= peak
    return np.stack([left, right], axis=1)


def crossfade(a: np.ndarray, b: np.ndarray, fade_s: float) -> np.ndarray:
    """a の末尾と b の先頭を fade_s 秒でクロスフェードして連結。"""
    f = int(fade_s * SR)
    f = min(f, len(a), len(b))
    if f <= 0:
        return np.concatenate([a, b], axis=0)
    w = np.linspace(0, 1, f).reshape(-1, 1)
    head = a[:-f]
    mid = a[-f:] * (1 - w) + b[:f] * w
    tail = b[f:]
    return np.concatenate([head, mid, tail], axis=0)


def generate(total_s: float = 240.0) -> np.ndarray:
    """total_s 秒の BGM を生成。"""
    # 各和音を ~32 秒で 16 秒クロスフェード、全体で total_s を超えるまで積む
    block_s = 32.0
    fade_s = 16.0
    out = None
    i = 0
    while True:
        cb = chord_block(CHORDS[i % len(CHORDS)], block_s)
        out = cb if out is None else crossfade(out, cb, fade_s)
        i += 1
        if len(out) / SR >= total_s + fade_s:
            break
    out = out[: int(total_s * SR)]
    # 全体の立ち上がり 3 秒、末尾 5 秒フェード
    env = np.ones(len(out))
    atk = int(3 * SR)
    rel = int(5 * SR)
    env[:atk] = np.linspace(0, 1, atk)
    env[-rel:] = np.linspace(1, 0, rel)
    return out * env.reshape(-1, 1)


def save_wav(path: Path, stereo: np.ndarray) -> None:
    # -18 dBFS あたりにノーマライズ（ナレーションを邪魔しない音量）
    peak = np.abs(stereo).max()
    if peak > 0:
        stereo = stereo / peak * 0.32
    pcm = (stereo * 32767.0).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="ukiyoe work slug (e.g., kanagawa_wave)")
    ap.add_argument("--duration", type=float, default=240.0, help="seconds")
    ap.add_argument("--out", default=None, help="override output path")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent.parent
    out_path = (
        Path(args.out) if args.out
        else repo / "public" / "ukiyoe" / args.name / "audio" / "bgm.wav"
    )
    print(f"[bgm] synthesizing {args.duration:.0f}s ...")
    audio = generate(args.duration)
    save_wav(out_path, audio)
    rel = out_path.relative_to(repo)
    print(f"[bgm] saved → {rel}  ({out_path.stat().st_size/1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
