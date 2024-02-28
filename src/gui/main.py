def main(frame_buffer) -> None:
    from src.gui.window import Window
    from typing import cast
    from multiprocessing import SimpleQueue
    import tkinter as t

    frame_buffer = cast(SimpleQueue, frame_buffer)
    root = t.Tk()
    app = Window(root, frame_buffer)

    app.root.mainloop()
