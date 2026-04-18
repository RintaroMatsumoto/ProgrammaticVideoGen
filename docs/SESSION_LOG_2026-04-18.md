# Session Log — 2026-04-18

浮世絵解説動画 MVP の仕上げとプラグイン化を実施。

## 1. プラグイン化：`programmatic-video-gen`

他の Cowork 利用者に配れる形にパッケージング。

- GitHub Issue #30 を起票
- スキル 2 本を同梱：
  - `ukiyoe-video`：特定の浮世絵作品から 6 シーン構成の解説動画を生成
  - `remotion-scene`：汎用 Remotion シーン（Ken Burns + 字幕 + ナレーション）
- テンプレート類をバンドル：
  - `scripts/`（脚本生成、音声合成、BGM 取得）
  - `src/components/`（KenBurns, BilingualSubtitle）
  - `src/compositions/UkiyoeAnimation.tsx`
  - `src/data/ukiyoe_scenes/`
- 成果物：`dist/programmatic-video-gen.plugin`（33 KB）

## 2. 演出のチューニング

見た目を「PowerPoint 風の安っぽさ」から「美術番組の引き」に寄せた。

- **Ken Burns**：ease-in-out（cubic）に変更。加減速を付けて、機械的な等速を排除
- **ビネット**：中央 55% を明るく、端に向け rgba(0,0,0,0.28) までグラデ
- **シネマ黒帯**：上 56 px / 下 260 px のグラデーションマット
- **和紙のざらつき**：SVG `fractalNoise` を data-URL で重ね、`mixBlendMode: overlay` / opacity 0.45
- **字幕**：
  - 左側 4 px アクセントバー（章ごとに色違い）
  - 章インジケータ `― 概観 / Overview ―` を薄く上部に
  - フェードアウトを 14→4f で前倒し、spring-in を柔らかく
  - タイトルシーンでは字幕非表示

章ごとの差し色は `title`/`overview`/`composition`/`technique`/`history`/`outro` の 6 種。

## 3. ナレーション

- VOICEVOX 起動後、`synthesize_narration.py` で 6 シーン分を再生成
- 話者：speaker=16（九州そら・ノーマル）
- `speedScale=0.96`、`prePhonemeLength=0.2`、`postPhonemeLength=0.3`

## 4. BGM：調達の旅

浮世絵と合う「静けさ」を求めて、三段階で試行錯誤した。

| 案 | 出所 | 判定 |
|---|---|---|
| 合成パッド（C ヨナ抜き） | 自作 | 初期仮組み。音楽的に退屈 |
| Debussy *La Mer*（BSO 1939） | Internet Archive | CC BY-NC-ND。商用不可で却下 |
| Debussy *L'Après-midi d'un faune*（Stokowski / Philadelphia, 1924） | Internet Archive / George Blood | 米・日・欧すべて PD。ただし 78 回転ノイズが目立つ |
| 同上＋`afftdn` 処理 | ffmpeg | RMS −6 dB、聴けるレベルに |
| **Erik Satie *Gymnopédie No.1*（Kevin MacLeod）** | incompetech.com | **採用**。CC BY 4.0 の現代ピアノ録音。クリーン |

### 処理パイプライン（最終版）

```
ffmpeg -i gymnopedie.mp3 -i gymnopedie.mp3 \
  -filter_complex "[0:a][1:a]acrossfade=d=12:c1=tri:c2=tri, \
                   atrim=0:240, \
                   afade=t=in:st=0:d=3, \
                   afade=t=out:st=235:d=5, \
                   loudnorm=I=-24:TP=-2:LRA=7" \
  -ac 2 -ar 44100 -sample_fmt s16 bgm.wav
```

平均 −26.4 dBFS、ピーク −4.0 dBFS。Remotion 側は `volume={0.18}` で混ぜる。

### 帰属

Kevin MacLeod の CC BY 4.0 は**公開時のクレジット表示が必須**。`public/ukiyoe/kanagawa_wave/CREDITS.md` に全出典とライセンスを集約済み。動画の概要欄・エンドカードに転記する。

```
"Gymnopedie No 1" by Kevin MacLeod (https://incompetech.com)
Licensed under Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/
```

### バックアップ

気分で戻せるように温存：

- `audio/bgm.wav.bak` — 初期の合成パッド
- `audio/bgm.debussy.wav` — Stokowski/Philadelphia 1924（ノイズ除去済）

## 5. コンポジションの統合

`UkiyoeAnimation.tsx` に BGM 再生を統合：

```tsx
{bgmPath && <Audio src={staticFile(bgmPath)} volume={bgmVolume} />}
```

`Root.tsx` の `defaultProps` に：

```tsx
bgmPath: "ukiyoe/kanagawa_wave/audio/bgm.wav",
bgmVolume: 0.18,
```

## 6. 積み残し

- [ ] Windows 側で最終レンダ：`npx remotion render UkiyoeKanagawaWave output\kanagawa_wave_satie.mp4`
- [ ] 再生確認（画質・音質・ナレーションとの被り）
- [ ] 気に入れば配布：`dist/programmatic-video-gen.plugin` を公開
- [ ] 次の浮世絵作品に同じパイプラインを適用

## 7. 参考

- Internet Archive: George Blood 78rpm Collection
- Music Modernization Act (2018) — 1924 年録音は 2025-01-01 に PD 化
- Kevin MacLeod / incompetech.com（CC BY 4.0）
- Musopen（SF 拠点の PD/CC0 クラシック音源）
