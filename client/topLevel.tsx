export function greenGeneralMessage(msg: string) {
  const elem = document.getElementById("message") as HTMLInputElement;
  if (!elem) return;
  elem.classList.add("green-text");
  elem.value = msg;
}

export function redGeneralMessage(msg: string) {
  const elem = document.getElementById("message") as HTMLInputElement;
  if (!elem) return;
  elem.classList.remove("green-text");
  elem.value = msg;
}
