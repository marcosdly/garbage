import tkinter as t
from src.gui.views.view import View
from multiprocessing import SimpleQueue
from PIL.ImageTk import PhotoImage  # type: ignore
from typing import Tuple


class VideoSection(t.Label):
    def __init__(
        self,
        parent: t.Widget,
        frame_buffer: SimpleQueue,
        size: Tuple[int, int],
    ):
        super().__init__(
            parent,
            background="#d6d6d6",
            borderwidth=2,
            foreground="#333",
            text="Video Not Found",
        )
        self.parent = parent
        self.frame_buffer = frame_buffer
        self.image_size = size
        self.grid_configure(row=0, column=0, sticky="nswe")

        self.after(1000 // 30, self.update_image)

    def update_image(self) -> None:
        if self.frame_buffer.empty():
            self.config(text="Buffering...")
            self.after(1000 // 30, self.update_image)
            return

        self.photo_image = PhotoImage(self.frame_buffer.get())
        self.config(image=self.photo_image)
        self.after(1000 // 30, self.update_image)


class VideoView(View):
    def __init__(self, parent: t.Widget, frame_buffer: SimpleQueue):
        super().__init__(parent)
        self.frame_buffer = frame_buffer
        width, height = size = (1052, 592)  # 30% of 1080p

        video = VideoSection(self, frame_buffer, size)
        self.columnconfigure(0, minsize=width)
        self.rowconfigure(0, minsize=height)
        video.grid()
