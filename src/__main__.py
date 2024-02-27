from multiprocessing import Process
from src.gui.main import main as tk_main


def main() -> None:
    tk = Process(target=tk_main, name="gui_entrypoint")

    tk.start()
    tk.join()


if __name__ == "__main__":
    main()
