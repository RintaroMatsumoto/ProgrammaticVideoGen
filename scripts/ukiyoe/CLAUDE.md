# scripts/ukiyoe/ — Claude 向け作業メモ

浮世絵パイプラインのスクリプト群を触るときのローカル規約。ルート CLAUDE.md と TOOLBOX.md の補遺。

## 起動順の鉄則

オーケストレータ `generate.py` を通す場合、実体の前提条件は以下の順に満たす：

1. 原画（`public/ukiyoe/<slug>/original.jpg`）が既に存在すること
2. **VOICEVOX エンジンが起動済み**（`http://127.0.0.1:50021/version` が 200 を返す）
3. `ANTHROPIC_API_KEY` が env に入っていること（脚本生成で使う）
4. `ffmpeg` が PATH に通っていること

いずれか欠けるとパイプライン途中でコケる。冒頭で `_healthcheck.py` を通す癖をつけること。

## ffmpeg のよく踏む地雷

| 症状 | 原因 | 対処 |
|---|---|---|
| concat で Non-monotonic DTS 警告連発 | 入力のサンプルレート不一致 | 事前に `-ar 44100` で揃える |
| `atrim` が効かない | `asetpts=PTS-STARTPTS` 入れ忘れ | filter_complex に必ず添える |
| `afftdn` で音が籠もる | `nr` が高すぎ（>20） | 18 前後で止める。それ以上は Q値を下げる |
| `loudnorm` 一発で不安定 | 2 pass 必要 | 短尺なら 1 pass で妥協。長尺は `-af loudnorm=print_format=json` で測定→係数固定 |

## VOICEVOX の呼び方

- 話者 ID はプロジェクト規約で **16（九州そら・ノーマル）** を既定（CONVENTIONS.md §1 に準拠）
- `speedScale=0.96`、`prePhonemeLength=0.2`、`postPhonemeLength=0.3` で落ち着かせる
- 固有名詞の読み崩れは `narration_ja` を**ひらがな化**して回避

## Internet Archive が必要な場合

- Cowork サンドボックスからは `archive.org` は allowlist 外。403 Forbidden
- **Desktop Commander で cmd.exe → curl** がワークアラウンド
- 識別子（`78_afternoon-of-a-faun-...`）は長いので truncation に注意。検索結果の表示は 60 文字で切れることがある

## musopen.org / incompetech.com

- Musopen は SPA。ページ HTML からは MP3 直リンクが取れない
- incompetech は静的 URL 発行。`https://incompetech.com/music/royalty-free/mp3-royaltyfree/<Title>.mp3`
- **CC BY 4.0 はクレジット必須**。帰属を忘れた動画は公開しない

## 出力ファイルの扱い

- `public/ukiyoe/<slug>/` 配下の `*.wav`、`*.jpg` は git に入れない（容量・LFS 未設定）
- `.cache/`・`.tmp_*`・`dist/` は `.gitignore` で除外済
- 生成物は再現スクリプトから作り直せる前提で運用

## ドキュメント側の書き込み先

- 作品単位の出典は `public/ukiyoe/<slug>/CREDITS.md`
- セッション横断の学びは `../../docs/SESSION_LOG_YYYY-MM-DD.md`
- 設計変更は `../../docs/adr/NNNN-*.md`
