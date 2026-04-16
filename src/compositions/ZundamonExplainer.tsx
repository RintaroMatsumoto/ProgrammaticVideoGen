import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import sceneData from "../data/scene_data.json";

interface SceneInfo {
  id: number;
  duration: number;
  text: string;
}

/* ── Background gradient ── */
const Background: React.FC = () => (
  <AbsoluteFill
    style={{
      background: "linear-gradient(135deg, #0f1923 0%, #1a2a3a 40%, #0d3320 100%)",
    }}
  />
);

/* ── Title bar (top) ── */
const TitleBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = spring({ frame, fps, from: 0, to: 1, durationInFrames: 20 });
  return (
    <div
      style={{
        position: "absolute",
        top: 40,
        left: 0,
        width: "100%",
        textAlign: "center",
        fontSize: 48,
        fontWeight: 900,
        color: "#7df28e",
        textShadow: "0 2px 12px rgba(0,0,0,0.7)",
        fontFamily: "'Noto Sans JP', sans-serif",
        opacity,
      }}
    >
      クロードのルーティーンって何？
    </div>
  );
};

/* ── Subtitle overlay (bottom) ── */
const Subtitle: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const y = spring({ frame, fps, from: 30, to: 0, durationInFrames: 12 });
  const opacity = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div
      style={{
        position: "absolute",
        bottom: 60,
        left: "50%",
        transform: `translateX(-50%) translateY(${y}px)`,
        background: "rgba(0,0,0,0.75)",
        borderRadius: 16,
        padding: "18px 48px",
        maxWidth: "85%",
        textAlign: "center",
        fontSize: 42,
        fontWeight: 700,
        color: "#fff",
        fontFamily: "'Noto Sans JP', sans-serif",
        textShadow: "0 1px 6px rgba(0,0,0,0.5)",
        opacity,
      }}
    >
      {text}
    </div>
  );
};

/* ── Animated character ── */
const AnimatedCharacter: React.FC<{ scene: SceneInfo }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pad = String(scene.id).padStart(2, "0");

  // Lip-sync: alternate mouth open/closed every 4 frames
  const mouthOpen = Math.floor(frame / 4) % 2 === 0;
  const charSrc = mouthOpen
    ? staticFile(`animated/char_${pad}_open.png`)
    : staticFile(`animated/char_${pad}_closed.png`);

  // Gentle bounce (breathing)
  const bounce = Math.sin(frame * 0.08) * 4;

  // Entrance spring
  const enterScale = spring({
    frame,
    fps,
    from: 0.9,
    to: 1,
    durationInFrames: 15,
    config: { damping: 12, stiffness: 120 },
  });
  const enterY = spring({
    frame,
    fps,
    from: 40,
    to: 0,
    durationInFrames: 15,
    config: { damping: 12, stiffness: 120 },
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 120,
        left: "50%",
        transform: `translateX(-50%) translateY(${bounce + enterY}px) scale(${enterScale})`,
        transformOrigin: "bottom center",
        height: "78%",
      }}
    >
      <Img
        src={charSrc}
        style={{
          height: "100%",
          width: "auto",
          objectFit: "contain",
          filter: "drop-shadow(0 8px 24px rgba(0,0,0,0.5))",
        }}
      />
    </div>
  );
};

/* ── Per-scene composition ── */
const ZundamonScene: React.FC<{ scene: SceneInfo }> = ({ scene }) => {
  const pad = String(scene.id).padStart(2, "0");
  return (
    <AbsoluteFill>
      <Background />
      <TitleBar />
      <AnimatedCharacter scene={scene} />
      <Subtitle text={scene.text} />
      <Audio src={staticFile(`audio/scene_${pad}.wav`)} />
    </AbsoluteFill>
  );
};

/* ── Main composition ── */
export const ZundamonExplainer: React.FC = () => {
  const { fps } = useVideoConfig();
  const scenes = sceneData.scenes as SceneInfo[];

  let currentFrame = 0;
  const timings = scenes.map((s) => {
    const from = currentFrame;
    const dur = Math.round(s.duration * fps) + 15;
    currentFrame += dur;
    return { ...s, from, dur };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {timings.map((s) => (
        <Sequence key={s.id} from={s.from} durationInFrames={s.dur}>
          <ZundamonScene scene={s} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
