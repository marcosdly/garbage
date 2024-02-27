import tkinter as t


class Window(t.Frame):
    def __init__(self, master: t.Tk) -> None:
        super().__init__(master)
        self.master = master
        self.root = master

        self.root.wm_title("TKinter Test - My Program")


root = t.Tk()
app = Window(root)
