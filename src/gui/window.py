import tkinter as t
from src.gui.views.tab_select import ViewSelector, ViewOption
from src.gui.views.config import ConfigView
from src.gui.views.video import VideoView
from multiprocessing import SimpleQueue
from typing import Callable, NamedTuple, Set


class Views(NamedTuple):
    config: ViewOption
    video: ViewOption


class Window(t.Frame):
    def __init__(self, master: t.Tk, frame_buffer: SimpleQueue) -> None:
        super().__init__(master)
        self.master = master
        self.root = master

        self.root.wm_title("TKinter Test - My Program")
        self.root.geometry("1280x768")
        self.root.resizable(width=False, height=False)
        # row 0 and column 0 will fill available space
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.grid(column=0, row=0, sticky=t.N + t.S + t.W + t.E)
        # row 1 and column 0 will fill available space
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        cfg = ConfigView(self)
        video = VideoView(self, frame_buffer)

        views = Views(
            ViewOption("config", cfg),
            ViewOption("video", video),
        )
        vs = ViewSelector(self, views, views.video.name)
        vs.grid()
