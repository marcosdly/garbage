import { StateRequest } from "./state.js";

class Section {
  name = "";

  constructor() {}

  apply(...node) {
    document.getElementById("section").append(...node);
  }

  clear() {
    document.getElementById("section").innerHTML = "";
  }

  register() {
    const btn = document.createElement("input");
    btn.type = "button";
    btn.value = this.name;
    btn.setAttribute("data-section-name", this.name);
    btn.classList.add("section-nav-button");
    btn.addEventListener("click", (event) => {
      event.preventDefault();
      name = event.currentTarget.getAttribute("data-section-name");
      this.clear();
      for (const sec of data_sections) {
        if (sec.name === name) {
          sec.apply();
        }
      }
    });
    data_sections.push(this);
    document.getElementById("section-nav").appendChild(btn);
  }
}

/** @type {Section[]} */
var data_sections = [];

class VideoSection extends Section {
  constructor() {
    super();
    this.name = "Video";
    this.original = this.#videoOutput("original");
    this.final = this.#videoOutput("final");
    this.state = this.#state();
  }

  apply() {
    super.apply(this.original, this.final, this.state);
  }

  #videoOutput(url_segment) {
    const title = document.createElement("h1");
    title.textContent = url_segment.toUpperCase();
    title.classList.add("video-title");
    const img = document.createElement("img");
    img.alt = `${url_segment} video output`;
    img.src = `/video/${url_segment}`;
    img.classList.add("video-output");
    const container = document.createElement("div");
    container.classList.add("video-container");
    container.append(title, img);
    return container;
  }

  #state() {
    const entrypointContainer = document.createElement("div");
    entrypointContainer.classList.add("state-container");
    const entrypointStart = document.createElement("input");
    entrypointStart.type = "button";
    entrypointStart.value = "Start";
    entrypointStart.classList.add("entrypoint-button");
    entrypointStart.addEventListener("click", (ev) => {
      ev.preventDefault();
      StateRequest.entrypoint.send("start");
    });
    const entrypointStop = document.createElement("input");
    entrypointStop.type = "button";
    entrypointStop.value = "Stop";
    entrypointStop.classList.add("entrypoint-button");
    entrypointStop.addEventListener("click", (ev) => {
      ev.preventDefault();
      StateRequest.entrypoint.send("stop");
    });

    entrypointContainer.append(entrypointStart, entrypointStop);
    return entrypointContainer;
  }
}

const video = new VideoSection();
video.register();
video.apply();
