import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  spring,
} from "remotion";

export const HelloWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Title animation: spring entrance
  const titleScale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 200 },
  });

  // Subtitle fade in after 30 frames
  const subtitleOpacity = interpolate(frame, [30, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Exit fade
  const exitOpacity = interpolate(
    frame,
    [durationInFrames - 30, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
        justifyContent: "center",
        alignItems: "center",
        opacity: exitOpacity,
      }}
    >
      <div
        style={{
          transform: `scale(${titleScale})`,
          textAlign: "center",
        }}
      >
        <h1
          style={{
            color: "#ffffff",
            fontSize: 80,
            fontWeight: 800,
            fontFamily: "sans-serif",
            margin: 0,
            textShadow: "0 4px 30px rgba(0,0,0,0.5)",
          }}
        >
          ProgrammaticVideoGen
        </h1>
        <p
          style={{
            color: "#a78bfa",
            fontSize: 36,
            fontWeight: 400,
            fontFamily: "sans-serif",
            marginTop: 20,
            opacity: subtitleOpacity,
          }}
        >
          Remotion + Claude Code
        </p>
      </div>
    </AbsoluteFill>
  );
};
