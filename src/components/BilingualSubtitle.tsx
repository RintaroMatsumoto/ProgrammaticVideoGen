import React from "react";
import {
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * 日英バイリンガル字幕。
 * 上段: 日本語（大きめ、明朝系）
 * 下段: 英語（細め、セリフ系）
 *
 * フェードイン 8f、フェードアウト 10f。ほのかな下からのスライド付き。
 */
export interface BilingualSubtitleProps {
  ja: string;
  en?: string;
  accent?: string; // 差し色（デフォルト藍色）
  chapter?: string; // 章名（例: 構図 / Composition）
}

export const BilingualSubtitle: React.FC<BilingualSubtitleProps> = ({
  ja,
  en,
  accent = "#a8c8e8",
  chapter,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const inP = spring({
    frame,
    fps,
    config: { damping: 200, stiffness: 140, mass: 0.5 },
  });
  const out = interpolate(
    frame,
    [durationInFrames - 14, durationInFrames - 4],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const opacity = Math.min(inP, out);
  const translateY = interpolate(inP, [0, 1], [22, 0]);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: 80,
        textAlign: "center",
        opacity,
        transform: `translateY(${translateY}px)`,
        pointerEvents: "none",
      }}
    >
      {chapter && (
        <div
          style={{
            display: "inline-block",
            marginBottom: 12,
            padding: "4px 16px",
            fontFamily:
              "'Noto Serif JP', 'Hiragino Mincho ProN', serif",
            fontSize: 22,
            color: accent,
            letterSpacing: "0.35em",
            textShadow: "0 2px 6px rgba(0,0,0,0.7)",
          }}
        >
          ― {chapter} ―
        </div>
      )}
      {ja && (
        <div
          style={{
            position: "relative",
            display: "inline-block",
            padding: "14px 36px 14px 44px",
            fontFamily:
              "'Noto Serif JP', 'Hiragino Mincho ProN', 'Yu Mincho', serif",
            fontSize: 52,
            fontWeight: 500,
            color: "#fafafa",
            background: "rgba(10, 14, 24, 0.72)",
            borderLeft: `4px solid ${accent}`,
            borderRadius: 2,
            letterSpacing: "0.04em",
            lineHeight: 1.35,
            textShadow: "0 2px 8px rgba(0,0,0,0.6)",
            maxWidth: "78%",
            boxShadow: "0 8px 28px rgba(0,0,0,0.4)",
          }}
        >
          {ja}
        </div>
      )}
      {en && (
        <div
          style={{
            marginTop: 10,
            display: "inline-block",
            padding: "8px 24px",
            fontFamily:
              "'EB Garamond', 'Times New Roman', Georgia, serif",
            fontSize: 30,
            fontStyle: "italic",
            color: "#e6ecf3",
            background: "rgba(10, 14, 24, 0.55)",
            borderRadius: 4,
            letterSpacing: "0.02em",
            maxWidth: "74%",
          }}
        >
          {en}
        </div>
      )}
    </div>
  );
};
