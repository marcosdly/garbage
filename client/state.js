var data_message = document.getElementById("message");

function blueMessage(msg) {
  data_message.classList.remove("red_text");
  data_message.classList.add("blue_text");
  data_message.textContent = msg;
}

function redMessage(msg) {
  data_message.classList.add("red_text");
  data_message.classList.remove("blue_text");
  data_message.textContent = msg;
}

class State {
  constructor(type) {
    this.type = type;
    this.request_url = window.origin + "/app/state";
  }

  send(state) {
    const init = {
      body: JSON.stringify({ type: this.type, state: state }),
      method: "POST",
      cache: "no-cache",
      headers: { "Content-Type": "application/json" },
    };
    const req = new Request(this.request_url, init);
    fetch(req).then(async (response) => {
      if (response.status >= 200 && response.status <= 299)
        blueMessage(response.status);
      else redMessage(response.status);
    });
  }
}

export class StateRequest {
  static entrypoint = new State("entrypoint");
}
