# CONVENTIONS.md — ProgrammaticVideoGen

プロジェクト固有の規約を一か所に集めたもの。Claudeは毎セッション冒頭でこのファイルも読むこと。

TOOLBOX.md が「環境の地雷対策」だとすれば、ここは「プロジェクト内の語彙と作法」。

---

## 1. ペルソナ・アンカー（Kuromi）

- 一人称：「わたくし」または「わたし」
- 二人称：「あなた」または「りんたろうくん」
- トーン：冷静沈着・知的・文学的・ツンデレ気味のウィット
- 長さ：短く端的。求められた以上のことは書かない
- 先回りしない。導きは問われたとき・道を外れたときに差し出す
- 箇条書きは必要最低限。散文を優先する

## 2. 用語集（JP / EN 固定訳）

翻訳の揺れは信用の揺れ。以下は本プロジェクトで通す表記。

| 日本語 | 英語（動画・字幕・ドキュメント共通） |
|---|---|
| 浮世絵 | ukiyo-e（ハイフンあり、小文字） |
| 錦絵 | nishiki-e |
| 木版画 | woodblock print |
| 富嶽三十六景 | *Thirty-six Views of Mount Fuji* |
| 神奈川沖浪裏 | *The Great Wave off Kanagawa* |
| 凱風快晴 | *Fine Wind, Clear Morning* |
| 東海道五十三次 | *The Fifty-three Stations of the Tōkaidō* |
| 葛飾北斎 | Katsushika Hokusai |
| 歌川広重 | Utagawa Hiroshige |
| 喜多川歌麿 | Kitagawa Utamaro |
| 東洲斎写楽 | Tōshūsai Sharaku |
| 構図 | composition |
| 技法 | technique |
| 概観 | overview |
| 歴史 | history |
| 結び | closing（章名として） |
| プルシアンブルー | Prussian blue（ベロ藍は Berlin blue と併記可） |
| 版木 | woodblock |
| 彫師 | block carver |
| 摺師 | printer |
| 絵師 | designer / artist |

長音符は原則マクロン（Hokusai、Tōkaidō）。人名は Wikipedia-en に合わせる。

## 3. シーン構成の既定

浮世絵解説動画は原則 6 章構成：

1. `title` — 作品名・作者
2. `overview` — 概観
3. `composition` — 構図
4. `technique` — 技法
5. `history` — 歴史
6. `outro` — 結び

章ごとのアクセント色は `src/compositions/UkiyoeAnimation.tsx` の `SECTION_META` を単一ソースとする。

## 4. コミット規約

```
feat: 新機能・新コンポジション
fix: バグ修正
chore: 設定・依存更新
docs: ドキュメント
refactor: 挙動不変のリファクタ
```

- 日本語 OK。ただし `git commit -m` 直打ちではなく `-F` でファイル経由
- スコープを括弧で：`feat(ukiyoe): ...`
- 該当 Issue があれば本文に `Refs #NN` / `Closes #NN`

## 5. 帰属テンプレート

公開時、動画概要欄・エンドカードに必ず転記する。

### BGM（現行：Satie / Kevin MacLeod）

```
"Gymnopedie No 1" by Kevin MacLeod (https://incompetech.com)
Licensed under Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/
```

### ナレーション（VOICEVOX）

```
Voice: VOICEVOX / 九州そら（ノーマル）
https://voicevox.hiroshiba.jp/
```

### 画像（浮世絵・PD）

```
Image: Katsushika Hokusai, "The Great Wave off Kanagawa", c. 1831.
Public domain.
```

作品ごとに差し替え。必ず作者没年の記載で PD の根拠を示す。

## 6. ファイル命名

- シーン JSON：`src/data/ukiyoe_scenes/<slug>.json`（例：`kanagawa_wave.json`）
- 素材ディレクトリ：`public/ukiyoe/<slug>/`
  - `original.jpg` — 元画像
  - `audio/scene_NN.wav` — シーンごとのナレーション
  - `audio/bgm.wav` — BGM
  - `CREDITS.md` — 作品ごとの帰属
- slug は半角英数＋アンダースコア。ハイフンは使わない

## 7. 何をしないか（Claude 向け）

- `public/ukiyoe/**/*.{wav,jpg,mp3}` をそのままコミットしない（大きい。LFS 検討）
- `.cache/`・`.tmp_*`・`dist/` はコミットしない（.gitignore で除外済）
- `src/assets/` 配下のキャラクター素材は touch しない（ずんだもん案件の領域）
- Issue を閉じる前に本 Convention に反する記述がないかセルフチェック
