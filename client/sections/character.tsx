import { useEffect, useState } from "preact/hooks";
import { greenGeneralMessage, redGeneralMessage } from "../topLevel";
import "./character.scss";
import { ChangeEvent } from "preact/compat";

interface CharState {
  base64: string;
  base64url: string;
  message: string;
}

interface ImageSelectArgs {
  id: string;
  title: string;
  type: "player" | "enemy";
  characterState: "front" | "back" | "dead";
}

function greenMessage(id: string) {
  const container = document.getElementById(id);
  if (!container) return;
  const msg = container.querySelector("char-imageselect-preview");
  if (!msg) return;
  msg.classList.add("green-text");
}

function redMessage(id: string) {
  const container = document.getElementById(id);
  if (!container) return;
  const msg = container.querySelector("char-imageselect-preview");
  if (!msg) return;
  // CSS hierarquy-based
  msg.classList.remove("green-text");
}

function ImageSelect({ id, title, type, characterState }: ImageSelectArgs) {
  const [state, setState] = useState({} as CharState);
  const requestUrl = window.origin + `/app/character/${type}/${characterState}`;
  const requestHeaders = {
    "Content-Transfer-Encoding": "base64",
  };

  const submit = async (ev: MouseEvent) => {
    ev.preventDefault();
    if (!state.base64 || !state.base64url) return;

    // type === "enemy"; frame === "front"
    const req = new Request(requestUrl, {
      body: state.base64,
      method: "POST",
      cache: "no-cache",
      keepalive: true,
      headers: requestHeaders,
    });

    await fetch(req).then((resp) => {
      if (resp.status === 200)
        greenGeneralMessage("Imagem enviada com sucesso");
      else redGeneralMessage("Erro ao enviar imagem");
    });
  };

  const pasteImage = async (ev: ClipboardEvent) => {
    ev.preventDefault();
    if (!ev.clipboardData) return;
    const files = ev.clipboardData.files;
    if (!files.length) return;
    const reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onloadend = () => {
      const url = reader.result as string;
      const base64 = url.split(",")[1];
      if (base64 === state.base64) return;
      let msg: string;

      if (base64 === state.base64) {
        msg = "Imagem é a selecionada";
        greenMessage(id);
      } else {
        msg = "Imagem não é a selecionada";
        redMessage(id);
      }

      setState({
        base64: base64,
        base64url: url,
        message: msg,
      });
    };
  };

  const placeholder = "Cole imagem aqui";
  const change = (ev: ChangeEvent) => {
    ev.preventDefault();
    (ev.currentTarget as HTMLInputElement).value = placeholder;
  };

  const setImage = () => {
    const req = new Request(requestUrl, {
      method: "GET",
      keepalive: true,
      headers: requestHeaders,
    });
    fetch(req).then(async (resp) => {
      if (resp.status === 200)
        greenGeneralMessage("Imagem de personagem buscada com sucesso");
      else {
        redGeneralMessage("Erro ao buscar imagem de personagem");
        return;
      }

      const encoded = await resp.text();

      setState({
        base64: encoded,
        base64url: `data:image/png;base64,${encoded}`,
        message: "",
      });
    });
  };

  useEffect(setImage, []);

  return (
    <>
      <div className="char-imageselect-container" id={id as string}>
        <h3 className="char-imageselect-title">{title as string}</h3>
        <img
          src={state.base64url}
          alt={`${type} ${characterState}`}
          className="char-imageselect-preview"
        />
        <input
          type="text"
          value={placeholder}
          onPaste={pasteImage}
          onChange={change}
          spellcheck={false}
          className="char-imageselect-button char-imageselect-paste"
        />
        <input
          type="button"
          value="Confirmar"
          onClick={submit}
          className="char-imageselect-button char-imageselect-submit"
        />
        <input
          type="button"
          value="Carregar original"
          onClick={setImage}
          className="char-imageselect-button"
        />
        <input
          type="text"
          value={state.message}
          disabled
          className="char-imageselect-message"
        />
      </div>
    </>
  );
}

function Player() {
  return (
    <>
      <div className="char-char-container char-player-container">
        <h2 className="char-char-title char-player-title">Player</h2>
        <div className="char-char-wrapper char-player-wrapper">
          <ImageSelect
            id="player-front"
            title="Frente"
            type="player"
            characterState="front"
          />
          <ImageSelect
            id="player-back"
            title="Costas"
            type="player"
            characterState="back"
          />
        </div>
      </div>
    </>
  );
}

function Enemy() {
  return (
    <>
      <div className="char-char-container char-enemy-container">
        <h2 className="char-char-title char-enemy-title">Inimigo</h2>
        <div className="char-char-wrapper">
          <ImageSelect
            id="enemy-front"
            title="Frente"
            type="enemy"
            characterState="front"
          />
          <ImageSelect
            id="enemy-back"
            title="Costas"
            type="enemy"
            characterState="back"
          />
          <ImageSelect
            id="enemy-dead"
            title="Morto"
            type="enemy"
            characterState="dead"
          />
        </div>
      </div>
    </>
  );
}

export function RenderCharacter() {
  return (
    <>
      <Player />
      <Enemy />
    </>
  );
}
