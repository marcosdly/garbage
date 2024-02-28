from multiprocessing import Process, SimpleQueue
from src.gui.main import main as tk_main
from src.video.main import main as video_main


def main() -> None:
    video_frame_buffer: SimpleQueue = SimpleQueue()
    tk = Process(target=tk_main, args=(video_frame_buffer,), name="gui_entrypoint")
    video = Process(
        target=video_main, args=(video_frame_buffer,), name="video_entrypoint"
    )

    video.start()
    tk.start()
    video.join()
    tk.join()


if __name__ == "__main__":
    main()
