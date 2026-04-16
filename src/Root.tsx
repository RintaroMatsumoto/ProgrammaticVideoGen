import { Composition } from "remotion";
import { HelloWorld } from "./compositions/HelloWorld";
import { ZundamonExplainer } from "./compositions/ZundamonExplainer";
import sceneData from "./data/scene_data.json";

// Calculate total duration from scene data
const totalDuration = sceneData.scenes.reduce(
  (acc, s) => acc + Math.round(s.duration * 30) + 15, // +15 padding per scene
  0
);

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
    </>
  );
};
