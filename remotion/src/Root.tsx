import { Composition } from "remotion";
import { SceneReel } from "./SceneReel";
import data from "./data.json";

/**
 * TWO COMPOSITIONS, ONE COMPONENT.
 *
 * The same source renders 16:9 and 9:16. That is deliberate and it is the thing most
 * people get wrong: a vertical cut is not a crop of the horizontal, it is a different
 * safe area — so the component reads its own dimensions and lays out accordingly.
 *
 * Duration comes from the STORYBOARD, in frames. `length_frames: 900` at 30fps is thirty
 * seconds. Writing 30 there gives you a one-second video, which is the first mistake
 * nearly everyone makes.
 */
export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="SceneReel"
      component={SceneReel}
      durationInFrames={data.lengthFrames}
      fps={data.fps}
      width={1920}
      height={1080}
    />
    <Composition
      id="SceneReelVertical"
      component={SceneReel}
      durationInFrames={data.lengthFrames}
      fps={data.fps}
      width={1080}
      height={1920}
    />
  </>
);
