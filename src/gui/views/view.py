import tkinter as t


class View(t.Frame):
    def __init__(self, parent, **kw) -> None:
        super().__init__(parent, **kw)
        self.parent = parent
        self.grid_configure(column=0, row=1, sticky=t.N + t.E + t.S + t.W)
