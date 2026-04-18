# 浮世絵アニメ自動生成パイプライン — 設計書

> **策定日**: 2026-04-18
> **関連Issue**: #14 [Phase 0] 主力艦単機でMVP動画を完全自動生成する
> **関連計画**: `docs/BUSINESS_PLAN.md` §4（チャンネルA）

---

## 1. 目的

浮世絵（最初は葛飾北斎『神奈川沖浪裏』）を **自動でアニメーション化し**、日本語ナレーション＋日英字幕付きの **3〜5分の解説動画** を生成するパイプライン。

「Moving Ukiyo-e」型（瀬川敦紀、Pasquale D'Amico）の手法を **AI で自動化**し、人手工程をゼロに近づける。

---

## 2. 基本方針

### 2.1 アニメーション方式：ハイブリッド 2.5D

| 構成要素 | 実現方法 |
|---|---|
| ベース演出 | Remotion による **2.5D パララックス** + **Ken Burns** |
| レイヤー分解 | **SAM2**（Segment Anything Model 2） |
| 深度推定 | **Depth Anything V2** |
| 隠れ背景補完 | **FLUX.1-schnell inpaint**（オプション） |
| 動的要素（波・雲） | **CogVideoX / Stable Video Diffusion**（オプション、部分適用） |

**非採用方針**：全編を AI 動画生成（Runway/Kling）に投げる方式は、浮世絵の木版画質感が崩れるため不採用。

### 2.2 音声・字幕

- **日本語ナレーション**：VOICEVOX（既存資産を再利用）
- **英語字幕**：Claude Opus 自身による翻訳
- **日本語字幕**：ナレーション同期表示
- **BGM**：PD/CC0 和楽（DOVA-SYNDROME、Musopen、甘茶の音楽工房）
- **SFX**：波音・風音（Freesound CC0）

### 2.3 動画構成（4分想定）

| 区間 | 時間 | 内容 |
|---|---|---|
| タイトル | 0:00–0:10 | 墨書き風ロゴ、和楽器スティンガー |
| 全体提示 | 0:10–0:30 | Ken Burns でゆっくりズーム |
| 構図解説 | 0:30–1:30 | 三分割・S字構図のガイド線オーバーレイ |
| 技法解説 | 1:30–2:30 | 彫り・摺りの拡大、色版分解アニメ |
| 歴史背景 | 2:30–3:30 | 当時の江戸地図、関連作品サムネ |
| アウトロ | 3:30–4:00 | まとめ＋次回予告＋チャンネル登録CTA |

---

## 3. ディレクトリ構成

```
ProgrammaticVideoGen/
├── src/
│   ├── compositions/
│   │   └── UkiyoeAnimation.tsx        # Remotion コンポジション（新規）
│   ├── components/
│   │   ├── ParallaxScene.tsx          # 2.5Dパララックス（新規）
│   │   ├── KenBurns.tsx               # カメラワーク（新規）
│   │   └── BilingualSubtitle.tsx     # 日英字幕（新規）
│   └── data/
│       └── ukiyoe_scenes/
│           └── kanagawa_wave.json     # シーン定義（新規）
├── public/
│   └── ukiyoe/
│       └── kanagawa_wave/
│           ├── original.jpg            # オリジナル画像
│           ├── layers/                 # SAM分解結果
│           │   ├── sky.png
│           │   ├── wave_main.png
│           │   ├── wave_back.png
│           │   ├── fuji.png
│           │   └── boats.png
│           ├── depth.png               # 深度マップ
│           └── audio/
│               ├── narration_ja.wav
│               ├── bgm.mp3
│               └── sfx_wave.mp3
├── scripts/
│   ├── ukiyoe/
│   │   ├── download_source.py         # Wikimedia ダウンロード
│   │   ├── generate_script.py         # Claude で脚本生成
│   │   ├── translate_subtitles.py     # 日→英翻訳
│   │   ├── segment_layers.py          # SAM2 分解
│   │   ├── estimate_depth.py          # Depth Anything V2
│   │   ├── inpaint_hidden.py          # FLUX inpaint（任意）
│   │   ├── synthesize_narration.py    # VOICEVOX TTS
│   │   └── generate.py                # オーケストレーター
│   └── ukiyoe_requirements.txt        # Python 依存
└── docs/
    └── UKIYOE_PIPELINE.md             # 本設計書
```

---

## 4. 処理フロー

```
┌────────────────────────────────────────────┐
│ Input: 作品名（例: "kanagawa_wave"）        │
└────────────────────────────────────────────┘
                 ↓
 ┌──────────────────────────────────────────┐
 │ Step 1. ソース取得                          │
 │  download_source.py                       │
 │  → Wikimedia Commons から高解像度PD画像     │
 │  → public/ukiyoe/<name>/original.jpg      │
 └──────────────────────────────────────────┘
                 ↓
 ┌──────────────────────────────────────────┐
 │ Step 2. 脚本生成                            │
 │  generate_script.py                       │
 │  → Claude API で日本語脚本（JSON）生成       │
 │  → src/data/ukiyoe_scenes/<name>.json     │
 └──────────────────────────────────────────┘
                 ↓
 ┌──────────────────────────────────────────┐
 │ Step 3. 英訳                                │
 │  translate_subtitles.py                   │
 │  → JSON の日本語を Claude で英訳追加        │
 └──────────────────────────────────────────┘
                 ↓
 ┌──────────────────────────────────────────┐
 │ Step 4. レイヤー分解（任意）                 │
 │  segment_layers.py                        │
 │  → SAM2 で主要領域を自動分解                │
 │  → public/ukiyoe/<name>/layers/*.png      │
 └──────────────────────────────────────────┘
                 ↓
 ┌──────────────────────────────────────────┐
 │ Step 5. 深度推定（任意）                     │
 │  estimate_depth.py                        │
 │  → Depth Anything V2 で depth map         │
 └──────────────────────────────────────────┘
                 ↓
 ┌──────────────────────────────────────────┐
 │ Step 6. ナレーション合成                    │
 │  synthesize_narration.py                  │
 │  → VOICEVOX で wav 生成                    │
 │  → public/ukiyoe/<name>/audio/*.wav       │
 └──────────────────────────────────────────┘
                 ↓
 ┌──────────────────────────────────────────┐
 │ Step 7. Remotion レンダリング                │
 │  npx remotion render UkiyoeAnimation      │
 │  → out/<name>.mp4                          │
 └──────────────────────────────────────────┘
```

---

## 5. MVP と本番の段階分け

### 5.1 MVP パス（本日完成目標）

**必要なもの**：
- Python 3.10+
- requests（ソース取得）
- VOICEVOX ローカル稼働
- Node.js + Remotion
- Claude API キー

**割愛するもの**（後付け可）：
- SAM2 分解 → **Ken Burns のみで演出**
- Depth Anything → **2Dパララックスなし**
- FLUX inpaint → 不要
- CogVideoX → 不要

MVPは **オリジナル画像1枚に Ken Burns + 日英字幕 + VOICEVOX ナレーション** で成立。

### 5.2 本番パス（Phase 1 以降）

- SAM2 で 4〜6レイヤー分解
- Depth Anything で 2.5D パララックス
- 波・雲に CogVideoX で動的演出
- タイトル・アウトロの演出強化

---

## 6. 技術的鍵所

### 6.1 Remotion コンポジション

- `<AbsoluteFill>` でフルスクリーンレイヤー
- `interpolate()` で Ken Burns（scale: 1.0 → 1.15、origin shift）
- レイヤー深度 → CSS transform translate3d で擬似3D
- 字幕は `<Sequence>` で時間制御、フェード in/out

### 6.2 脚本 JSON スキーマ

```json
{
  "meta": {
    "title_ja": "神奈川沖浪裏",
    "title_en": "Under the Wave off Kanagawa",
    "artist": "葛飾北斎",
    "year": 1831,
    "source_url": "https://..."
  },
  "scenes": [
    {
      "id": 1,
      "section": "title",
      "duration": 10,
      "narration_ja": "...",
      "narration_en": "...",
      "subtitle_ja": "...",
      "subtitle_en": "...",
      "camera": { "zoom": 1.0, "x": 0.5, "y": 0.5 },
      "overlays": []
    },
    ...
  ]
}
```

### 6.3 レイヤー命名規約（SAM 分解後）

```
sky.png         : 空
fuji.png        : 富士山
wave_back.png   : 奥の波
wave_main.png   : 手前の主要波
boats.png       : 舟群
foam.png        : 飛沫（任意）
```

---

## 7. 外部ソース

### 7.1 PD 画像取得候補（優先順）

1. **Metropolitan Museum of Art Open Access**（API あり、CC0）
2. **Library of Congress**（高解像度、PD明記）
3. **Wikimedia Commons**（安定、複数作品カバー）
4. **Art Institute of Chicago API**（CC0）

### 7.2 音楽

- **DOVA-SYNDROME** 和風カテゴリ（商用可、クレジット表記推奨）
- **Musopen** 邦楽PD
- **YouTube Audio Library** "Traditional Japanese"

### 7.3 効果音

- **Freesound.org**（CC0 フィルタ）
- **zapsplat**（無料会員制）

---

## 8. 品質基準（MVP合格ライン）

- [ ] 人手介入ゼロで動画が出力される
- [ ] 動画時間 3〜5分
- [ ] 日本語ナレーションが違和感なく聞こえる
- [ ] 日本語・英語字幕が同期して表示される
- [ ] 著作権表記・出典クレジットがアウトロに含まれる
- [ ] 画像の上下左右ズレ・カクつきがない

---

## 9. 既知の制限とフォローアップ

| 制限 | 対応 |
|---|---|
| SAM2 未セットアップ時は Ken Burns のみ | 後日 setup.sh で自動化 |
| FLUX inpaint はGPU必須 | Colab フォールバック検討 |
| Musopen のダウンロードURL変動 | 定数化して一元管理 |
| YouTube Content ID 誤爆 | 配信前に DMCA セーフ BGM のみ選定 |

---

## 10. 次の一手

1. 本設計書の実装（Phase 0 完了目標）
2. 神奈川沖浪裏 の MVP 動画レンダリング・QA
3. レンダ時間・品質の測定 → Issue #14 に記録
4. 次題材：『富嶽三十六景』他の景（凱風快晴、山下白雨）
