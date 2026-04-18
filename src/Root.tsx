import { Composition } from "remotion";
import { HelloWorld } from "./compositions/HelloWorld";
import { ZundamonExplainer } from "./compositions/ZundamonExplainer";
import {
  UkiyoeAnimation,
  computeUkiyoeDuration,
  UkiyoeData,
} from "./compositions/UkiyoeAnimation";
import sceneData from "./data/scene_data.json";
import kanagawaWave from "./data/ukiyoe_scenes/kanagawa_wave.json";

// Calculate total duration from scene data
const totalDuration = sceneData.scenes.reduce(
  (acc, s) => acc + Math.round(s.duration * 30) + 15, // +15 padding per scene
  0
);

const FPS = 30;
const ukiyoeKanagawa = kanagawaWave as unknown as UkiyoeData;
const ukiyoeKanagawaFrames = computeUkiyoeDuration(ukiyoeKanagawa, FPS);

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ZundamonExplainer"
        component={ZundamonExplainer}
        durationInFrames={totalDuration}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="UkiyoeKanagawaWave"
        component={UkiyoeAnimation}
        durationInFrames={ukiyoeKanagawaFrames || 300}
        fps={FPS}
        width={1920}
        height={1080}
        defaultProps={{
          name: "kanagawa_wave",
          data: ukiyoeKanagawa,
          bgmPath: "ukiyoe/kanagawa_wave/audio/bgm.wav",
          bgmVolume: 0.18,
        }}
      />
    </>
  );
};
