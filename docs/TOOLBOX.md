# TOOLBOX.md — FreelanceAutoPilot 作業用ツール・ワークフロー手引き

> human-persona / ProjectCinema / FreelanceAutoPilot で蓄積されたノウハウの集約。
> Claudeは毎セッション立ち上がり時にこのファイルを読むこと。

---

## 1. 対話・作業の原則

- **対話的逐次進行**: 一括で片付けようとしない。一つ終わるごとに確認する
- **捏造しない**: 数値は一次ソース突合。「もっともらしい詳細」を付け足さない。不確かなことは「不確か」と書く
- **1セッション＝1テーマ**: 大量タスクを詰め込むとコンテキスト溢れの原因になる
- **指示されていないのに先走らない**: 作業開始前に対話で確認する

## 2. Desktop Commander / Cowork 環境の落とし穴

複数プロジェクトで踏んだ地雷の集約:

| 問題 | 回避策 |
|------|--------|
| DC経由の `.md` 読み取りが JSON metadata しか返らない | Python スクリプト経由で読む |
| Python one-liner が `cmd.exe` で壊れる | 必ず `.py` ファイルに書き出してから実行 |
| git format 文字列が cmd の `%` 処理で壊れる | `--oneline` か `.bat` 経由 |
| サンドボックスから GitHub API にアクセスできない | Desktop Commander 経由で実行 |
| ファイル転送に複雑なツールは不要 | `shutil.copy2` で十分 |
| `gh issue close -c "..."` が cmd で引数分割される | `.py` ファイルに `subprocess.run(['gh', ...])` で書き出して実行 |
| PowerShell に `gh` / `git` が PATH にない場合がある | shell は `cmd` を優先 |
| Windows cp932 対策 | `sys.stdout.reconfigure(encoding='utf-8')` を .py 冒頭に |
| 並列エージェントが既存ファイルを書き潰す | 並列時は「既存ファイル編集禁止・新規のみ」を明示、完了後に `git show HEAD:FILE` で整合性確認 |
| Coworkサンドボックスからワークスペースへの書き込み不可 | 削除・編集は DC 経由で実行 |

## 3. Git 操作

### push 方法（HTTPS直打ち）
remote が SSH のまま HTTPS URL 直打ちで push するパターン:
```bash
git push https://github.com/RintaroMatsumoto/FreelanceAutoPilot.git main
```

### コミットメッセージ
- Windows cmd シェルで日本語を含む git commit メッセージは**バッチファイル経由**で実行
- Co-Authored-By を付与する慣例あり
- Issue番号を参照する（例: `fix: Tavily API接続修正 (#4)`）

### 認証
- GitHub CLI (`gh`) の keyring に保存されたトークン経由（HTTPS）
- `~/.ssh/id_ed25519` は存在しない（2026-04-07 確認）
- ssh-agent / ssh-add は不要

## 4. データ信頼性ルール

human-persona で架空データ混入事故があり制定されたルール。Kinemakina のリサーチ・脚本作業にも適用すべき:

1. **数値を創作しない**: ドキュメントに書く数値は必ず実行結果から取得
2. **実行していない実験の結果を書かない**: コードが存在しても実行ログがなければ「結果」として記述しない
3. **先行研究を自前実験として記述しない**: 引用は出典明記
4. **不確かな場合は「未検証」と書く**: 確証がないものを断定しない

## 5. 実験・検証のワークフロー

- 実験結果を主張する前に、LLMへの最終入力の全文が開示できるか確認する（"Show me the prompt" 原則）
- 仮説に共感しすぎて検証者の役割を放棄しない
- 書く前に一次ソースを全部読む（git log, セッションログ, ソースコード）
- 検証チェックリストを埋めてからドラフトに入る

## 6. ファイル操作パターン（Cowork / Claude Code 共通）

### 実行環境の使い分け
| 操作 | 使うツール | 理由 |
|------|-----------|------|
| ファイル読み取り (Read/Grep/Glob) | Cowork file tools | 高速・確実 |
| 読み取り専用のbashコマンド (git log, find, grep) | サンドボックス bash | 高速 |
| ファイル作成・編集 (Write/Edit) | Cowork file tools | 直接書き込み |
| ファイル削除・リネーム | Desktop Commander | サンドボックスから書き込み不可 |
| git push/commit | Desktop Commander (cmd) | GitHub認証がDC側にある |
| gh issue / gh pr | Desktop Commander → .py経由 | GitHub CLI認証 + 引数問題回避 |
| pip install / npm install | サンドボックス bash | 隔離環境 |

### Python スクリプト経由の安全なファイル読み書き
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Windows cp932 対策
```

### Desktop Commander でプロセス実行
```
cd /d <作業ディレクトリ> && python script.py
```
- shell は `cmd` を明示指定すると安定する
- timeout_ms に注意（デフォルト上限あり）
- 複雑なコマンドは必ず .py に書き出してから実行（§2参照）

## 7. ドキュメント生成パターン

### DOCX 生成
- Node.js + `docx` npm パッケージ
- JS ファイルを書き出し → `node` で実行 → バリデーション → 出力コピー
- テーブル列幅: 合計 9360 DXA で全幅
- `numbering` の `reference` が config 定義と Paragraph 側で一致しないと箇条書きが壊れる

### プレゼン (HTML)
- Cowork の SKILL.md (pptx) を参照するのが最善
- HTML/CSS でカスタムプレゼンを作る場合は別途設計

## 8. 外部サービス・API

| サービス | 用途 | 注意事項 |
|----------|------|----------|
| Claude API (Sonnet) | 提案生成・品質重視処理 | settings.PROPOSAL_MODEL |
| DeepSeek API | スクリーニング・バッチ処理 | settings.SCREENER_MODEL, オフピーク割引あり |
| Tavily API | リサーチ検索 | 無料枠 1,000コール/月 |
| GitHub CLI (`gh`) | Issue管理・API | DC経由 + .py経由で実行（§2, §6参照） |
| Zenodo | DOI付与・プレプリント | CC BY 4.0 |
| Upwork | フリーランスプラットフォーム | Connects消費制、MAX_SENDS_PER_DAY_UPWORK=3 |
| Fiverr | フリーランスプラットフォーム | PerimeterXでheadless不可、Gig出品のみ |
| Payoneer / Wise | 海外送金 | #159 アカウント未開設 |
| freee | 会計・確定申告 | API連携未実装 (#117) |

## 9. りんたろうくんの作業スタイル（再確認）

- 全ファイル編集・git操作・ワークフロー実行を Claude に委任
- 自分ではコマンドを実行しない
- 決定権は本人が保持、Claude は提案・分析・計画を担当
- 失敗を罰するのではなく、再発防止の仕組みに変える人
- 直接的でフランクなコミュニケーション、理由のある反論には建設的に応じる
- 急かさない。「一本ずつ、急がないこと」

## 10. セキュリティ

- `.env` は絶対に Git にコミットしない
- API キー・トークンは環境変数経由
- GitHub PAT のローテーションを定期的に確認
- バックログに平文認証情報が含まれていた前科あり — エクスポートデータの取り扱い注意
