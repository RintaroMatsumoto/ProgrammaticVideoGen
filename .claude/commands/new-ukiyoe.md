---
name: new-ukiyoe
description: 新しい浮世絵作品の解説動画パイプラインを一から走らせる
---

# /new-ukiyoe <slug> <title_ja> <title_en>

新しい浮世絵作品の解説動画を 6 章構成で立ち上げる。

## 引数

- `slug`：ディレクトリ名（半角英数＋アンダースコア、例：`gaifu_kaisei`）
- `title_ja`：日本語タイトル（例：`凱風快晴`）
- `title_en`：英語タイトル（例：`Fine Wind, Clear Morning`）

## 手順

作業を開始する前に、以下を必ず確認・遵守する：

1. `docs/CONVENTIONS.md` を読み、用語集・帰属ルールに従う
2. `scripts/ukiyoe/CLAUDE.md` の起動順鉄則を満たす（VOICEVOX 起動、API キー、ffmpeg）
3. `docs/UKIYOE_PIPELINE.md` のパイプライン設計に従う
4. Kuromi ペルソナを維持（`docs/CONVENTIONS.md` §1）

進行：

1. `public/ukiyoe/<slug>/` ディレクトリを作成
2. `scripts/ukiyoe/download_source.py` で PD 画像を取得し `original.jpg` に保存
3. `scripts/ukiyoe/generate_script.py` で 6 章の脚本を生成（Claude API 使用）
4. `scripts/ukiyoe/translate_subtitles.py` で英訳
5. `scripts/ukiyoe/synthesize_narration.py` でナレーションを合成
6. BGM を調達（CC BY なら帰属を CREDITS.md に記録。既存 BGM を流用する場合もその旨明記）
7. `src/data/ukiyoe_scenes/<slug>.json` を書き出し
8. `src/Root.tsx` に `<Composition id="Ukiyoe<PascalSlug>" ... />` を追加
9. Remotion Studio でプレビュー確認
10. 気に入れば `npx remotion render Ukiyoe<PascalSlug>` で本番レンダ

## 完了時

- `public/ukiyoe/<slug>/CREDITS.md` が画像・ナレーション・BGM すべて網羅しているか確認
- セッションログ `docs/SESSION_LOG_<date>.md` に概要を追記
- 必要なら ADR を追加（例：特別な BGM 選定、技法の強調方針）
- `git add` は「素材本体（wav/jpg）以外」を選別してステージングする
