import { SectionButton, sections } from "./sections/section";
import { useState } from "preact/hooks";

export function App() {
  const [Section, setSection] = useState(() => sections["video"]);

  return (
    <>
      <nav id="section-nav">
        <SectionButton name="video" setState={setSection} />
        <SectionButton name="character" setState={setSection} />
      </nav>
      <div id="message-container">
        <input id="message" type="text" disabled></input>
      </div>
      <div id="section">
        <Section />
      </div>
    </>
  );
}
