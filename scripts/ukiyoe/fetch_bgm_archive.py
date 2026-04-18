#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Internet Archive (archive.org) から Debussy の PD 録音を取得し、
BGM 用の wav に加工する。

US Music Modernization Act (2018) により、1923 年以前の録音は 2022 年に
PD 入り済み。1924 〜 1946 年の録音は「公開年 +100 年」で順次 PD 入りする。
2026 年時点で 1925 年までの録音は PD。

Defaults は 1924 年の Stokowski / Philadelphia Symphony による
L'Après-midi d'un Faune（牧神の午後への前奏曲）2 パート。
しっとり漂う音色で浮世絵との相性は抜群。
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_ITEMS = [
    # (identifier, preferred file extension, part label)
    ("78_afternoon-of-a-faun-part-1-laprs-midi-dun-faune_philadelphia-symphony-orchestr_gbia0489440a",
     "flac", "1/2"),
    ("78_afternoon-of-a-faun-part-2-laprs-midi-dun-faune_philadelphia-symphony-orchestr_gbia0489440b",
     "flac", "2/2"),
]


def fetch_metadata(identifier: str) -> dict:
    url = f"https://archive.org/metadata/{identifier}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def pick_file(meta: dict, ext: str) -> str | None:
    wanted = {"flac": ("Flac", "FLAC"), "mp3": ("VBR MP3", "64Kbps MP3", "MP3")}
    fmts = wanted.get(ext, ("Flac",))
    best = None
    best_size = -1
    for f in meta.get("files", []):
        if f.get("format") in fmts:
            sz = int(f.get("size", 0) or 0)
            if sz > best_size:
                best = f["name"]
                best_size = sz
    return best


def download(identifier: str, filename: str, dst: Path) -> None:
    url = f"https://archive.org/download/{identifier}/" + urllib.request.quote(filename)
    print(f"[dl] {url}")
    urllib.request.urlretrieve(url, dst)


def ffmpeg_concat_and_trim(parts: list[Path], out: Path, duration: float) -> None:
    """連結 → トリム → 78 回転盤のノイズ除去 → フェード → ラウドネス正規化 → 44.1kHz wav。

    78rpm シェラック盤特有のパチパチ・ヒスを段階的に抑える:
      1. highpass 80Hz: サブソニックの低域ゴロ
      2. lowpass  7200Hz: シェラック盤の高域ヒスと帯域外ノイズ
      3. afftdn:   FFT ベースのスペクトル減算 (-25dB 床, 18dB 削減)
      4. compand:  緩いノイズゲート兼ダイナミクス整形
      5. loudnorm: 最終ラウドネス正規化 (-26 LUFS: BGM として控えめ)
    """
    concat_list = out.parent / "_concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in parts), encoding="utf-8"
    )
    fade_out_start = max(0.0, duration - 5.0)
    af = (
        "highpass=f=80,"
        "lowpass=f=7200,"
        "afftdn=nf=-25:nr=18:nt=w,"
        f"afade=t=in:st=0:d=3,"
        f"afade=t=out:st={fade_out_start}:d=5,"
        "loudnorm=I=-26:TP=-3:LRA=7"
    )
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-t", f"{duration}",
        "-af", af,
        "-ac", "2", "-ar", "44100", "-sample_fmt", "s16",
        str(out),
    ]
    print(f"[ffmpeg] concat+denoise+trim → {out.name}")
    subprocess.run(cmd, check=True)
    concat_list.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="ukiyoe slug (e.g. kanagawa_wave)")
    ap.add_argument("--duration", type=float, default=240.0)
    ap.add_argument("--out-name", default="bgm.wav")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent.parent
    audio_dir = repo / "public" / "ukiyoe" / args.name / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    # 作業ディレクトリ
    cache = repo / ".cache" / "bgm"
    cache.mkdir(parents=True, exist_ok=True)

    downloaded: list[Path] = []
    for ident, ext, label in DEFAULT_ITEMS:
        print(f"\n[ia] fetching {ident}  part {label}")
        meta = fetch_metadata(ident)
        md = meta.get("metadata", {})
        print(f"  title: {md.get('title')}")
        print(f"  year : {md.get('year') or md.get('date')}")
        print(f"  license: {md.get('licenseurl','(no explicit license)')}")
        fname = pick_file(meta, ext)
        if not fname:
            print(f"  [warn] no {ext} file found, trying mp3")
            fname = pick_file(meta, "mp3")
        if not fname:
            print(f"  [skip] no audio file")
            continue
        local = cache / f"{ident}{Path(fname).suffix.lower()}"
        if not local.exists():
            download(ident, fname, local)
        else:
            print(f"  [cache] {local.name}")
        downloaded.append(local)

    if not downloaded:
        print("[error] no source audio downloaded")
        return 1

    out_wav = audio_dir / args.out_name
    backup = audio_dir / (args.out_name + ".bak")
    if out_wav.exists() and not backup.exists():
        out_wav.rename(backup)
        print(f"[backup] previous bgm → {backup.name}")

    ffmpeg_concat_and_trim(downloaded, out_wav, args.duration)
    print(f"\n[ok] {out_wav}  ({out_wav.stat().st_size/1024/1024:.1f} MB)")
    print("[credit] Debussy, L'Après-midi d'un faune")
    print("         Leopold Stokowski / The Philadelphia Orchestra, 1924")
    print("         Public domain in the US under the Music Modernization Act")
    print("         Source: https://archive.org/details/georgeblood")
    return 0


if __name__ == "__main__":
    sys.exit(main())
