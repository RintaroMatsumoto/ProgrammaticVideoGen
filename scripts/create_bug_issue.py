import subprocess, os
os.chdir(r"C:\Users\GoldRush\Documents\MyProject\ProgrammaticVideoGen")

title = "バグ修正記録: PSDレイヤー名不一致による表情パーツ消失"
body = r"""## 症状
特定のシーンでずんだもんの**目が消える**。全12シーンのうち6シーン（2, 3, 5, 6, 8, 10）で発生。

## 原因
スクリプトJSON (`scripts/zundamon_routine_explainer.json`) で目の表情を `"eyes": "普通目"` と指定していたが、PSDファイル内の実際のレイヤー名は `*目セット` だった。

`set_expression()` が `*普通目` を探してどのレイヤーにもマッチしない → 全目レイヤーが `visible=False` になる → 目が消える。

### PSD側のレイヤー構造（!目グループ）
```
*目セット      ← デフォルト表情（普通の目）★これが正解
*にっこり
*にっこり2
*ジト目
*なごみ目
*細め目
*細め目ハート
*上向き / *上向き2 / *上向き3
*ぐるぐる / *〇〇 / *UU / *><
```

「普通目」「ノーマル」等の直感的な名前は存在しない。デフォルトは `目セット`。

## 修正（634bc10）
```diff
- "eyes": "普通目"
+ "eyes": "目セット"
```
全6箇所を一括置換。

## 再発防止策
1. **新しい表情を追加する前に `scripts/check_layers.py` でPSDレイヤー名を確認する**
2. `generate_animated_assets.py` の `set_expression()` でマッチするレイヤーが見つからなかった場合に警告を出すバリデーション追加を推奨
3. 四国めたん対応時（#3）も同様のレイヤー名ミスマッチに注意

## 関連ファイル
- `scripts/check_layers.py` — PSDレイヤー名をUTF-8テキストで出力するユーティリティ
- `scripts/layers.txt` — ずんだもん立ち絵PSDの全表情レイヤー名一覧
- `scripts/generate_animated_assets.py` — PSD composite生成スクリプト

## 教訓
PSD立ち絵素材のレイヤー命名規則は作者依存。「普通」「ノーマル」「デフォルト」等の汎用名ではなく、素材固有の名前（この場合「目セット」）が使われていることがある。**必ず実レイヤー名を確認してからスクリプトを書くこと。**
"""

r = subprocess.run(
    ["gh", "issue", "create",
     "--title", title,
     "--body", body,
     "--label", "bug"],
    capture_output=True, text=True, encoding="utf-8"
)
print(r.stdout.strip())
if r.stderr:
    print(r.stderr.strip())
