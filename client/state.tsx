const data_message = document.getElementById("message");

function blueMessage(msg: any) {
  if (!data_message) return;
  data_message.classList.remove("red_text");
  data_message.classList.add("blue_text");
  data_message.textContent = msg;
}

function redMessage(msg: any) {
  if (!data_message) return;
  data_message.classList.add("red_text");
  data_message.classList.remove("blue_text");
  data_message.textContent = msg;
}

class State {
  type: string;
  request_url: string;

  constructor(type: string) {
    this.type = type;
    this.request_url = window.origin + "/app/state";
  }

  send(state: string) {
    const req = new Request(this.request_url, {
      body: JSON.stringify({ type: this.type, state: state }),
      method: "POST",
      cache: "no-cache",
      headers: { "Content-Type": "application/json" },
    });

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
