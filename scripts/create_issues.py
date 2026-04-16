import subprocess, os
os.chdir(r"C:\Users\GoldRush\Documents\MyProject\ProgrammaticVideoGen")

issues = [
    {
        "title": "テンプレート化: 汎用ずんだもん解説動画ジェネレーター",
        "body": """## 概要
現在はクロードルーティーン専用のスクリプトだが、任意のトピックで解説動画を生成できるテンプレートシステムにする。

## タスク
- [ ] スクリプトJSON仕様の汎用化（トピック、シーン数、表情パターンをパラメータ化）
- [ ] CLIまたはAPI入力 → スクリプトJSON自動生成
- [ ] 背景テーマ/カラーパレットの設定機能
- [ ] テンプレートからMP4までの1コマンド実行パイプライン""",
        "labels": "enhancement"
    },
    {
        "title": "四国めたん対応: マルチキャラクター動画生成",
        "body": """## 概要
四国めたんの立ち絵PSD素材も配置済み。複数キャラクターでの掛け合い動画に対応する。

## タスク
- [ ] 四国めたんPSDレイヤー解析・表情マッピング
- [ ] スクリプトJSONにspeaker/character指定を追加
- [ ] VOICEVOX四国めたんvoice_id統合
- [ ] 2キャラ同時表示のRemotionレイアウト（左右配置）
- [ ] 掛け合いシーンのタイミング制御""",
        "labels": "enhancement"
    },
    {
        "title": "YouTube自動アップロード機能",
        "body": """## 概要
生成したMP4をYouTube Data API v3で自動アップロードする。

## タスク
- [ ] Google OAuth2認証フロー実装
- [ ] YouTube Data API v3 Python clientでアップロード
- [ ] タイトル/説明文/タグの自動生成
- [ ] サムネイル自動生成（動画の1フレーム + テキストオーバーレイ）
- [ ] アップロードスケジュール機能""",
        "labels": "enhancement"
    },
    {
        "title": "音声品質向上: VOICEVOX話速・イントネーション調整",
        "body": """## 概要
現在はデフォルトパラメータでVOICEVOX合成している。シーンの感情に合わせた話速・ピッチ調整を行う。

## タスク
- [ ] audio_queryのspeedScale/pitchScale/intonationScaleをシーンごとに設定可能に
- [ ] 感情タグ（excited, calm, sad等）→ パラメータ自動マッピング
- [ ] シーン間のポーズ（無音）長さ調整
- [ ] 8種のボイススタイル使い分け（ノーマル/あまあま/ツンツン等）""",
        "labels": "enhancement"
    },
    {
        "title": "アニメーション強化: 表情トランジション・ジェスチャー",
        "body": """## 概要
現在のアニメーションはリップシンク+バウンスのみ。より豊かな動きを追加する。

## タスク
- [ ] シーン内での表情変化（途中で目や眉が変わる）
- [ ] 指差しジェスチャーのタイミング制御
- [ ] フェード/スライドによるシーントランジション
- [ ] 強調時の拡大アニメーション
- [ ] 記号レイヤー（汗、涙、アヒルちゃん）のアニメーション表示""",
        "labels": "enhancement"
    },
    {
        "title": "CI/CD: GitHub Actions自動レンダリング",
        "body": """## 概要
スクリプトJSON をpushしたら自動でレンダリング→成果物としてMP4を生成するCI。

## タスク
- [ ] GitHub Actionsワークフロー作成
- [ ] VOICEVOX Dockerイメージ or APIモック
- [ ] Remotion Lambda or ローカルレンダリング
- [ ] MP4をGitHub Releasesにアタッチ
- [ ] PSD素材のキャッシュ戦略""",
        "labels": "enhancement"
    },
]

for i, issue in enumerate(issues):
    print(f"Creating issue {i+1}: {issue['title']}")
    r = subprocess.run(
        ["gh", "issue", "create",
         "--title", issue["title"],
         "--body", issue["body"],
         "--label", issue["labels"]],
        capture_output=True, text=True, encoding="utf-8"
    )
    print(f"  stdout: {r.stdout.strip()}")
    if r.stderr:
        print(f"  stderr: {r.stderr.strip()}")
    print()
