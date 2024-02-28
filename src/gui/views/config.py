import tkinter as t
from src.gui.views.view import View


class ConfigView(View):
    def __init__(self, parent) -> None:
        super().__init__(parent, background="#1f75fe")
