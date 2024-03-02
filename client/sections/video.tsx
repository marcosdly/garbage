import { StateRequest } from "../state";
import "./video.scss";

function VideoOutput({ url_segment }: Record<string, string>) {
  url_segment = url_segment as string;
  return (
    <div className="video-container">
      <h1 className="video-title">{url_segment.toUpperCase()}</h1>
      <video src="" className="video-output"></video>
    </div>
  );
}

function VideoState() {
  const listener = (ev: MouseEvent) => {
    ev.preventDefault();
    const entrypoint = (ev?.currentTarget as HTMLElement)?.getAttribute(
      "data-entrypoint",
    );
    if (entrypoint) StateRequest.entrypoint.send(entrypoint);
  };

  return (
    <div className="state-container">
      <input
        type="button"
        data-entrypoint="start"
        value="Start"
        className="entrypoint-button"
        onClick={listener}
      />
      <input
        type="button"
        data-entrypoint="stop"
        value="Stop"
        className="entrypoint-button"
        onClick={listener}
      />
    </div>
  );
}

export function RenderVideo() {
  return (
    <>
      <VideoOutput url_segment={"original"} />
      <VideoOutput url_segment={"final"} />
      <VideoState />
    </>
  );
}
