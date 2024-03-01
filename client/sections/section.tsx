import { RenderVideo } from "./video";
import { FunctionComponent } from "preact";

export const sections: Record<string, FunctionComponent> = {
  video: RenderVideo,
};

export function SectionButton({ name, setState }: any) {
  return (
    <input
      type="button"
      value={name}
      className="section-nav-button"
      onClick={() => setState(() => sections[name])}
    />
  );
}
