import { SectionButton, sections } from "./sections/section";
import { useState } from "preact/hooks";

export function App() {
  const [Section, setSection] = useState(() => sections["video"]);

  return (
    <>
      <nav id="section-nav">
        <SectionButton name={"video"} setState={setSection} />
      </nav>
      <div id="message-container">
        <p id="message"></p>
      </div>
      <div id="section">
        <Section />
      </div>
    </>
  );
}
