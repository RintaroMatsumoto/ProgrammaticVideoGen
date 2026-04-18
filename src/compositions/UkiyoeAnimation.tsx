import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useVideoConfig,
} from "remotion";
import { KenBurns } from "../components/KenBurns";
import { BilingualSubtitle } from "../components/BilingualSubtitle";

/**
 * 浮世絵解説動画のRemotionコンポジション (MVP)。
 *
 * データは src/data/ukiyoe_scenes/<name>.json。
 * MVPではKen Burnsのみ（ParallaxSceneはPhase 2で切替）。
 *
 * 使い方:
 *   Root.tsx 側で <Composition component={UkiyoeAnimation}
 *     defaultProps={{name: "kanagawa_wave"}} ... />
 *   とデフォルトプロップで作品名を渡すか、動的ロードする。
 *
 * 静的requireだとビルド時に作品追加ができないため、
 * Rootでjsonをimportしてpropsに渡す形にしている。
 */

export interface UkiyoeCamera {
  zoom: number;
  x: number;
  y: number;
  endZoom?: number;
  endX?: number;
  endY?: number;
  tilt?: number;
}

export interface UkiyoeScene {
  id: number;
  section: string;
  duration: number; // seconds
  narration_ja: string;
  subtitle_ja: string;
  narration_en?: string;
  subtitle_en?: string;
  camera: UkiyoeCamera;
  audio_path?: string;
  overlays?: unknown[];
}

export interface UkiyoeMeta {
  title_ja: string;
  title_en: string;
  artist: string;
  year: number;
}

export interface UkiyoeData {
  meta: UkiyoeMeta;
  scenes: UkiyoeScene[];
}

export interface UkiyoeAnimationProps {
  name: string;
  data: UkiyoeData;
  /** BGM ファイルのパス (public/ 相対)。未指定なら鳴らさない */
  bgmPath?: string;
  /** BGM 音量 0..1。既定 0.18 (ナレーションを邪魔しない程度) */
  bgmVolume?: number;
}

/**
 * 章ごとの演出メタデータ。
 * accent: 字幕の差し色 / chapter: 字幕上部に薄く出る章名
 */
const SECTION_META: Record<
  string,
  { accent: string; chapter?: string }
> = {
  title:       { accent: "#e8d4a8" },
  overview:    { accent: "#b8cfe5", chapter: "概観 / Overview" },
  composition: { accent: "#d4b58c", chapter: "構図 / Composition" },
  technique:   { accent: "#6ea5c8", chapter: "技法 / Technique" },
  history:     { accent: "#c4a878", chapter: "歴史 / History" },
  outro:       { accent: "#e8b8a0", chapter: "結び / Closing" },
};

// 和紙のざらつきを擬似的に乗せる SVG ノイズ（data URL）
const PAPER_GRAIN =
  "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='5'/><feColorMatrix values='0 0 0 0 0.92 0 0 0 0 0.88 0 0 0 0 0.78 0 0 0 0.09 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")";

/**
 * シーン単体のレンダラ。
 */
const SceneView: React.FC<{
  name: string;
  scene: UkiyoeScene;
}> = ({ name, scene }) => {
  const originalSrc = staticFile(`ukiyoe/${name}/original.jpg`);
  const cam = scene.camera;
  const fromZoom = cam.zoom ?? 1.0;
  const toZoom = cam.endZoom ?? Math.max(fromZoom, fromZoom + 0.06);
  const fromXY = { x: cam.x ?? 0.5, y: cam.y ?? 0.5 };
  const toXY = {
    x: cam.endX ?? cam.x ?? 0.5,
    y: cam.endY ?? cam.y ?? 0.5,
  };
  const meta = SECTION_META[scene.section] ?? SECTION_META.overview;
  const isTitle = scene.section === "title";

  return (
    <AbsoluteFill>
      <KenBurns
        src={originalSrc}
        fromZoom={fromZoom}
        toZoom={toZoom}
        fromXY={fromXY}
        toXY={toXY}
        tilt={cam.tilt ?? 0}
      />
      {/* 和紙のざらつき（全シーン共通の微ノイズ） */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: PAPER_GRAIN,
          backgroundSize: "300px 300px",
          mixBlendMode: "overlay",
          opacity: 0.45,
          pointerEvents: "none",
        }}
      />
      {/* 上下の黒帯（シネマスコープ風） */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 56,
          background: "linear-gradient(180deg, rgba(0,0,0,0.9), rgba(0,0,0,0))",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 260,
          background: "linear-gradient(0deg, rgba(0,0,0,0.88), rgba(0,0,0,0))",
          pointerEvents: "none",
        }}
      />
      {!isTitle && (
        <BilingualSubtitle
          ja={scene.subtitle_ja}
          en={scene.subtitle_en}
          accent={meta.accent}
          chapter={meta.chapter}
        />
      )}
    </AbsoluteFill>
  );
};

/**
 * タイトル専用オーバーレイ（section="title" のシーンに重ねる）。
 */
const TitleOverlay: React.FC<{ meta: UkiyoeMeta }> = ({ meta }) => (
  <AbsoluteFill
    style={{
      justifyContent: "center",
      alignItems: "center",
      background:
        "radial-gradient(ellipse at center, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.55) 100%)",
    }}
  >
    <div
      style={{
        textAlign: "center",
        padding: "28px 60px",
        background: "rgba(8, 12, 22, 0.55)",
        border: "1px solid rgba(255,255,255,0.2)",
      }}
    >
      <div
        style={{
          fontFamily:
            "'Noto Serif JP', 'Hiragino Mincho ProN', 'Yu Mincho', serif",
          fontSize: 96,
          color: "#fafafa",
          letterSpacing: "0.12em",
          fontWeight: 600,
          textShadow: "0 4px 12px rgba(0,0,0,0.8)",
        }}
      >
        {meta.title_ja}
      </div>
      <div
        style={{
          marginTop: 14,
          fontFamily: "'EB Garamond', 'Times New Roman', serif",
          fontSize: 38,
          fontStyle: "italic",
          color: "#d8e0ea",
          letterSpacing: "0.08em",
        }}
      >
        {meta.title_en}
      </div>
      <div
        style={{
          marginTop: 28,
          fontFamily:
            "'Noto Serif JP', 'Hiragino Mincho ProN', serif",
          fontSize: 32,
          color: "#c9d2dd",
        }}
      >
        {meta.artist} ・ {meta.year}
      </div>
    </div>
  </AbsoluteFill>
);

/**
 * メインコンポジション。
 */
export const UkiyoeAnimation: React.FC<UkiyoeAnimationProps> = ({
  name,
  data,
  bgmPath,
  bgmVolume = 0.18,
}) => {
  const { fps } = useVideoConfig();

  let cursor = 0;
  const seqs = data.scenes.map((scene) => {
    const frames = Math.round(scene.duration * fps);
    const start = cursor;
    cursor += frames;
    return { scene, start, frames };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* BGM は全シーン通して流す */}
      {bgmPath && (
        <Audio src={staticFile(bgmPath)} volume={bgmVolume} />
      )}
      {seqs.map(({ scene, start, frames }) => (
        <Sequence
          key={scene.id}
          from={start}
          durationInFrames={frames}
          name={`scene-${scene.id}-${scene.section}`}
        >
          <SceneView name={name} scene={scene} />
          {scene.section === "title" && <TitleOverlay meta={data.meta} />}
          {scene.audio_path && (
            <Audio src={staticFile(scene.audio_path)} />
          )}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

/**
 * durationInFrames 算出ヘルパ。Root.tsx から呼ぶ。
 */
export const computeUkiyoeDuration = (
  data: UkiyoeData,
  fps: number
): number => {
  return data.scenes.reduce(
    (acc, s) => acc + Math.round(s.duration * fps),
    0
  );
};
