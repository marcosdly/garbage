import tkinter as t
from os import path
from PIL import ImageGrab, ImageChops, Image, ImageTk  # type: ignore
import cv2 as cv


class CharacterSelect(t.LabelFrame):
    def __init__(self, parent: t.Widget, label: str, filename: str) -> None:
        super().__init__(parent, text=label)
        self.parent = parent
        self.filename = filename
        self.path = path.abspath(f"state/characters_select/{filename}")
        self.image_size = (256, 256)
        self.width, self.height = self.image_size
        self.photo_image: ImageTk.PhotoImage | None = None

        self.columnconfigure(0, minsize=self.width)
        self.rowconfigure(0, minsize=self.height)
        self.grid_configure(padx=5, pady=5)

        self.preview = t.Label(
            self,
            text="Aguardando imagem...",
            background="#d6d6d6",
            foreground="#333",
            image=self.photo_image if self.photo_image else None,  # type: ignore
        )
        self.paste = t.Button(
            self, text="Colar Imagem", command=self.on_paste, padx=10, pady=5
        )
        self.submit = t.Button(
            self, text="Confirmar", command=self.on_submit, padx=10, pady=5
        )
        self.message = t.Label(self, text="", background="#eee")

        if path.isfile(self.path):
            img = Image.fromarray(cv.imread(self.path, cv.IMREAD_COLOR))
            self.put_image(img)

        self.preview.grid(column=0, row=0, padx=5, pady=5, sticky="nswe")
        self.paste.grid(column=0, row=1, padx=5, pady=5, sticky="we")
        self.submit.grid(column=0, row=2, padx=5, pady=5, sticky="we")
        self.message.grid(column=0, row=3, padx=5, pady=5, sticky="we")

    def on_paste(self) -> None:
        img = ImageGrab.grabclipboard()
        if img is None:
            self.red_message("Sem imagem para copiar")
            return
        self.put_image(img)

    def on_submit(self) -> None:
        ImageTk.getimage(self.photo_image).save(self.path)
        self.compare()

    def compare(self) -> None:
        if not path.isfile(self.path):
            self.red_message("Imagem não é a selecionada")
            return
        diff = ImageChops.difference(
            Image.open(self.path), ImageTk.getimage(self.photo_image)
        )
        if not diff.getbbox():
            self.green_message("Imagem é a selecionada")
        else:
            self.red_message("Imagem não é a selecionada")

    def put_image(self, img: Image) -> None:
        img = img.resize(self.image_size, Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(img)
        self.preview.config(image=self.photo_image)
        self.compare()

    def red_message(self, msg: str) -> None:
        self.message.config(foreground="#f00", text=msg, image=None)  # type: ignore

    def gray_message(self, msg: str) -> None:
        self.message.config(foreground="#333", text=msg, image=None)  # type: ignore

    def green_message(self, msg: str) -> None:
        self.message.config(foreground="#0c00ba", text=msg, image=None)  # type: ignore
