# Architecture Decision Records

短く、日付入りで、「なぜそれを選んだか」を残す場所。

## 書式

```
# ADR-NNNN: タイトル

- Date: YYYY-MM-DD
- Status: proposed | accepted | superseded by ADR-MMMM
- Context: 何を決めなければならなかったか
- Decision: 何を選んだか
- Consequences: 良い面・悪い面・トレードオフ
```

## 運用ルール

- 一つの ADR は A4 一枚相当（~40 行以内）に収める
- 覆すときは新しい ADR を書いて旧 ADR を `superseded by` にする。消さない
- 過去の決定を再議論する誘惑に負けそうなときは、該当 ADR を読む

## 索引

- [ADR-0001: Remotion を動画生成基盤に採用](./0001-remotion-over-moviepy.md)
- [ADR-0002: ナレーションに VOICEVOX を採用](./0002-voicevox-for-narration.md)
- [ADR-0003: BGM に Kevin MacLeod の Gymnopédie No.1 を採用](./0003-satie-gymnopedie-for-bgm.md)
