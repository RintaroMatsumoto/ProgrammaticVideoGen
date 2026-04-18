# ADR-0001: Remotion を動画生成基盤に採用

- Date: 2026-04-15（推定。プロジェクト初期）
- Status: accepted

## Context

Programmatic な動画生成には複数の選択肢がある：

- **Remotion**：React/TSX で動画を記述、Chromium ヘッドレスでレンダ
- **MoviePy**：Python、FFmpeg ラッパー、命令的 API
- **FFmpeg 直叩き**：最強・最低レベル、複雑な合成は地獄
- **Manim**：数学アニメ特化、UI が貧弱
- **After Effects + ExtendScript**：商用、ライセンス必要

## Decision

**Remotion** を採用する。

## Consequences

良い面：
- React 経験が活きる。レイアウトとアニメを宣言的に書ける
- 字幕・カメラ・オーバーレイの合成が CSS / Tailwind で完結
- Studio による即時プレビューが速い
- Claude が TSX を書きやすい（学習データが豊富）

悪い面：
- Chromium レンダで CPU/メモリ消費が大きい（4 分動画で数 GB）
- Web 向けライブラリ（Three.js 等）の癖を学ぶ必要
- 商用利用は会社規模で有償ライセンスが要る（個人利用は無料）

トレードオフ：
- 純 FFmpeg より遅いが、保守性は段違い
- Python パイプライン（脚本生成・音声合成）と TS レンダの二言語構成になる
  → スクリプト類は `scripts/`、レンダは `src/` で物理的に分離して回避
