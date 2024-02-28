import tkinter as t


class Window(t.Frame):
    def __init__(
        self,
        master: t.Tk,
    ) -> None:
        super().__init__(master)
        self.master = master
        self.root = master

        self.root.wm_title("TKinter Test - My Program")
        self.root.geometry("1280x768")
        self.root.resizable(width=False, height=False)
        self.root.grid()
        self.grid(column=0, row=0, sticky=t.N + t.S + t.W + t.E)


root = t.Tk()
app = Window(root)
