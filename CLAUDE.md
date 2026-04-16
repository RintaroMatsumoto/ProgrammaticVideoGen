# CLAUDE.md — ProgrammaticVideoGen

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
