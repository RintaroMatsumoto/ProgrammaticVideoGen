# ADR-0003: BGM に Kevin MacLeod の Gymnopédie No.1 を採用

- Date: 2026-04-18
- Status: accepted（最初の浮世絵作品「神奈川沖浪裏」での採用。他作品は別途検討）

## Context

浮世絵解説動画の BGM 候補：

| 案 | 出所 | ライセンス | 音質 | 判定 |
|---|---|---|---|---|
| 自作合成パッド | スクリプト生成 | 自由 | 退屈 | 仮組み |
| Debussy *La Mer* (BSO 1939) | Internet Archive | CC BY-NC-ND | 良 | **商用不可で却下** |
| Debussy *L'Après-midi d'un Faune* (Stokowski 1924) | Internet Archive | PD（米日欧） | 78rpm 由来のパチパチ | アナログ感は良いが解説向きでない |
| 同上 + `afftdn` 処理 | ffmpeg | PD | 改善 | 採用候補 |
| **Erik Satie *Gymnopédie No.1*（Kevin MacLeod）** | incompetech.com | **CC BY 4.0** | **クリーン** | **採用** |

## Decision

Kevin MacLeod の *Gymnopédie No.1* を採用。Debussy 版は `audio/bgm.debussy.wav` として温存。

## Consequences

良い面：
- 現代録音の解像度。ノイズなし
- Satie の三拍子の揺らぎが浮世絵の静けさと共鳴
- 名曲なので視聴者にも親しみやすい
- 著作権処理が単純（CC BY 帰属表示一行）

悪い面：
- CC BY なので公開時にクレジット必須（忘れると規約違反）
- ピアノ独奏で音域が狭く、長尺だと単調になりがち
  → 240 秒には acrossfade で 2 周させて尺を確保
- 同曲を多用するとチャンネルの音楽的個性が薄れる
  → 作品ごとに BGM を変える運用（次作品で別曲を選定）

トレードオフ：
- PD 録音にこだわれば帰属不要だが、音質を取った
- 「クレジット表示の徹底」という運用負荷を引き受ける代わりに、現代録音のクリーンさを得る

## 関連

- `public/ukiyoe/kanagawa_wave/CREDITS.md`
- `docs/CONVENTIONS.md` §5「帰属テンプレート」
