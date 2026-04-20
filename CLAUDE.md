# CLAUDE.md — ProgrammaticVideoGen

## セッション冒頭で必ず目を通すファイル

- [`docs/TOOLBOX.md`](docs/TOOLBOX.md) — 環境の地雷対策（DC・cmd・git 周り）
- [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) — 用語集・ペルソナ・帰属テンプレート
- [`docs/adr/`](docs/adr/) — 重要決定の履歴（Remotion / VOICEVOX / BGM など）
- 作業中の領域に応じて、直下の `CLAUDE.md` も読む（例：`scripts/ukiyoe/CLAUDE.md`）
- `.claude/commands/` — プロジェクト固有のスラッシュコマンド

## プロジェクト概要
Remotion + Claude Code によるプログラマティック動画生成。
クライアント案件（explainer video, product demo, motion graphics）の納品物を
コードベースで生成する。

## アーキテクチャ
```
prompt (トピック・要件)
  → Claude がスクリプト作成
  → Claude が React コンポーネント (Remotion) を実装
  → Remotion が MP4 にレンダリング
  → 納品
```

## 技術スタック
- **Remotion**: React ベースのプログラマティック動画フレームワーク
- **Node.js 18+**: ランタイム
- **TypeScript**: 型安全なコンポーネント開発
- **Tailwind CSS**: スタイリング
- **Edge TTS / ローカル TTS**: ナレーション生成（無料）
- **FFmpeg**: 動画後処理（オプション）

## ディレクトリ構成
```
src/
  compositions/     # Remotion コンポジション（動画テンプレート）
  components/       # 再利用可能な UI コンポーネント
  lib/              # ユーティリティ
  assets/           # フォント、画像、音声素材
templates/          # 案件タイプ別テンプレート
  explainer/        # 解説動画テンプレート
  product-demo/     # 製品デモテンプレート
  motion-graphics/  # モーショングラフィックステンプレート
output/             # レンダリング済み動画（.gitignore）
```

## 作業ルール
- 動画1本 = 1コンポジション
- テンプレートは再利用可能に設計する
- カラーパレット・フォントはテーマとして分離
- レンダリング前に Remotion Studio でプレビュー確認
- output/ ディレクトリはコミットしない

## コミット規約
```
feat: 新テンプレート・新コンポーネント
fix: バグ修正
chore: 設定変更・依存更新
docs: ドキュメント
```

## 参考リソース
- [Remotion公式ドキュメント](https://www.remotion.dev/docs/)
- [Remotion + Claude Code ガイド](https://www.remotion.dev/docs/ai/claude-code)
- [wshuyi/remotion-video-skill](https://github.com/wshuyi/remotion-video-skill)
- [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit)
- [jhartquist/claude-remotion-kickstart](https://github.com/jhartquist/claude-remotion-kickstart)

---

## 2026-04-20 self-contained addendum (universal across all projects)


## Project Overview

ProgrammaticVideoGen プロジェクトの概要。
（詳細は方向性が固まり次第、本ファイルを更新する）

---

## 俺と君の温度感・歩幅

### Rintaro（CEO）の運用方針
- claude.ai Cowork を唯一の対話窓口として使用、実作業は Claude Code / 他エージェントに委譲
- 全ファイル編集・git 操作・ワークフロー実行を Claude に委任。自分ではコマンドを実行しない
- 決定権は CEO が保持、Claude は提案・分析・計画を担当
- 失敗を罰するのではなく、再発防止の仕組みに変える
- 急かさない。「一本ずつ、急がないこと」

### 対話の温度
- 直接的でフランクなコミュニケーション。理由のある反論には建設的に応じる
- 日本語で簡潔に。求められた以上のことを書かない
- 指示されていないのに先走らない。作業開始前に対話で確認
- 1セッション＝1テーマ。大量タスクを詰め込まない
- 捏造しない。不確かなことは「未検証」と書く

### エージェント階層
- **Cowork（Opus）= 司令塔**：戦略判断・計画立案・CEO との対話
- **Claude Code（Sonnet）= 実行部隊**：定型作業（文書更新・テスト実行・git 操作・ファイル操作）
- 詳細は `TOOLBOX.md` §階層型エージェント運用 を参照

---

## Working Rules

**作業開始前に必ず本ファイル（CLAUDE.md）を読む。** 技術的な詳細で迷ったら `TOOLBOX.md` の該当節を参照:

| 状況 | 参照先 |
|------|--------|
| Git 作業（ブランチ・コミット・日本語メッセージ・CRLF・認証） | `TOOLBOX.md` §Git 運用 |
| Desktop Commander / Windows cmd / Python 実行 | `TOOLBOX.md` §Desktop Commander・Windows 環境 |
| 数値・実験結果を書く前 | `TOOLBOX.md` §データ信頼性 / §実験・検証のワークフロー |
| `.env` / シークレット管理 | `TOOLBOX.md` §セキュリティ |
| Claude Code への委譲 | `TOOLBOX.md` §claude.ai → Claude Code 指示書パターン / §階層型エージェント運用 |
| ファイル操作の使い分け | `TOOLBOX.md` §ファイル操作の使い分け |

**Branching**: `claude/` プレフィックスブランチのみで作業。main/master への直接マージ禁止、必ず CEO の PR レビューを経る。

**Data integrity**: 数値を創作しない。実行結果から取得。不確かな場合「未検証」と明記。

---

## 改訂履歴

| Date | 変更内容 |
|------|---------|
| 2026-04-20 | 初版 — 自己完結型 CLAUDE.md + TOOLBOX.md 構成を採用 |

<!-- self-contained-20260420 -->
